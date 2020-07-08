import grpc
from google.protobuf import empty_pb2

import base_pb2
import AsrService_pb2
import AsrService_pb2_grpc

import sounddevice as sd
import soundfile as sf
import samplerate as sr
import numpy as np
from queue import Queue
import sys
import argparse
import keyboard
import curses


def create_default_input_stream(user_callback, user_blocksize=None):
    # Получаем дефолтные настройки дефолтного микрофона
    input_device = sd.query_devices(kind="input")
    microphone_name = input_device["name"]
    microphone_samplerate = input_device["default_samplerate"]
    microphone_channels = input_device["max_input_channels"]

    # Если у вас не работает захват звука с дефолтного микрофона, то придётся самостоятельно подбирать устройство и его настройки
    # См. python -m sounddevice и код выше
    return sd.InputStream(dtype="int16", blocksize=user_blocksize, callback=user_callback)


def test_callback(indata, frames, time, status):
    pass


def check_default_input_device():
    try:
        input_stream = create_default_input_stream(user_callback=test_callback)
        input_stream.close()
        print("Default input device checked!")
    except Exception as ex:
        print("check_default_input_device failed! Exception: {}\n !!! See create_default_input_stream() !!!".format(ex))
        sys.exit(1)


def recognize_from_micro(model_name, block_size_ms):
    # Конфигурируем распознавание на модель model_name и частоту model_samplerate
    yield AsrService_pb2.RecognizeRequest(config=AsrService_pb2.RecognitionConfig(
        auth=AsrService_pb2.Auth(
            client_id=args.client_id,
            domain_id=args.domain_id,
            api_key=args.api_key
        ),
        model=base_pb2.Model(id=model_name)))

    model_samplerate = 8000 if 'phone_call' in model_name.lower() or 'ivr' in model_name.lower() else 16000

    # Получаем частоту дискретизации дефолтного микрофона
    microphone_samplerate = 0
    with create_default_input_stream(user_callback=test_callback) as input_device:
        microphone_samplerate = input_device.samplerate

    # Очередь звуковых данных
    queue = Queue()

    # Callback для обработки очередной порции звука, пришедшей с микрофона
    def capture_sound_callback(indata, frames, time, status):
        if status:
            print(status, flush=True)
        queue.put(indata.copy())

    # Сколько сэмлов будем брать с микрофона
    bsize_micro = int(microphone_samplerate * block_size_ms / 1000.0)

    # Для передискретизации звука
    screen.addstr("microphone samplerate: {} \n".format(microphone_samplerate))
    screen.refresh()
    resampling_ratio = float(model_samplerate) / microphone_samplerate
    resampler = sr.Resampler(converter_type="sinc_best")

    screen.addstr("Press Q for quit\n\n")
    screen.refresh()

    # Параллельно будем писать в файл, чтобы проверить захват звука
    with sf.SoundFile("recorded.wav", mode="w", samplerate=int(model_samplerate),
                      channels=1, subtype="PCM_16") as file:

        with create_default_input_stream(user_blocksize=bsize_micro, user_callback=capture_sound_callback):
            while True:
                raw_sound_from_microphone = queue.get()


                # Выбираем только один канал и делаем передискретизацию на целевую частоту модели распознавания речи
                _, cols = raw_sound_from_microphone.shape
                raw_sound = raw_sound_from_microphone[:, :-1] if cols > 1 else raw_sound_from_microphone
                sound_for_recognition = \
                    resampler.process(raw_sound, resampling_ratio).astype(np.int16)

                # Отправляем звук на распознавание
                yield AsrService_pb2.RecognizeRequest(
                    sound=AsrService_pb2.Sound(samples=sound_for_recognition.tobytes()))

                file.write(sound_for_recognition)

                # Завершаем запись при нажатии клавиши
                if keyboard.is_pressed("q"):
                    break

    # Завершаем распознавание
    yield AsrService_pb2.RecognizeRequest(finish=base_pb2.Finish())


def erase_text(py, px, qy, qx, screen):
    """Стереть порцию текста между заданными координатами"""

    # Определим текущие размеры окна консоли
    num_rows, num_cols = screen.getmaxyx()

    # Проверим корректность входных аргументов
    if py > qy:
        return
    if py == qy:
        if px == qy:
            return
    space = " "

    # Если кусок находится в одной строке (переноса не было)
    if py == qy:
        # Очищаем данные в этой строке
        for x in range(px, qx):
            screen.addstr(py, x, space)
    # Если был перенос текста на другую строку
    else:
        # Очищаем строку, с которой началась запись куска текста
        for x in range(px, num_cols):
            screen.addstr(py, x, space)

        # Очищаем строки посередине (если есть)
        if qy - py > 1:
            for y in range(py + 1, qy):
                for x in range(0, num_cols):
                    screen.addstr(y, x, space)

        # Очищаем строку, на которой закончилась запись куска текста
        for x in range(0, qx):
            screen.addstr(qy, x, space)

    screen.refresh()


def add_lines_if_end(py, qy, text, screen):
    """Добавить заданное количество пустых строк, если достигнут конец окна"""
    rows, cols = screen.getmaxyx()
    y, x = screen.getyx()
    lines_count = 10

    if y == rows - 1:
        if x + len(text) >= cols:
            for i in range(lines_count):
                screen.addstr(y, x, '\n')
            screen.refresh()
            py -= lines_count
            qy -= lines_count
    return py, qy


if __name__ == '__main__':
    # Командные аргументы
    parser = argparse.ArgumentParser()
    parser.add_argument("model_name", type=str, help="Model ID for recognition")
    parser.add_argument("--blocksize", type=int, default=200, help="Duration of each block of sound (ms), default: 200")
    parser.add_argument("--client_id", type=str, help="Client ID/username, typically email address")
    parser.add_argument("--api_key", type=str, help="API access key")
    parser.add_argument("--domain_id", type=str, help="Domain ID")
    args = parser.parse_args()

    model_name = args.model_name
    block_size_ms = args.blocksize

    # Проверка захвата звука с дефолтного микрофона
    # !!! ПРОВЕРКА ОБЯЗАТЕЛЬНО ДОЛЖНА ПРОХОДИТЬ !!!
    # Дальше в коде производится захват звука с дефолтного микрофона
    check_default_input_device()

    # Инициализация библиотеки работы с консолью
    screen = curses.initscr()
    screen.scrollok(True)
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)


    # Соединяемся с сервером
    creds = grpc.ssl_channel_credentials()
    channel = grpc.secure_channel('asr.cp.speechpro.com', creds)
    # Будем использовать сервис распознавания речи
    speech_recognizer = AsrService_pb2_grpc.SpeechRecognitionStub(channel)

    # Получаем список всех доступных моделей
    model_list = speech_recognizer.GetListOfSpeechRecognitionModels(
        AsrService_pb2.Auth(
            client_id=args.client_id,
            domain_id=args.domain_id,
            api_key=args.api_key
        ))
    screen.addstr("All available speech recognition models:\n".format(model_list))
    for model in model_list.models:
        screen.addstr("{}\n".format(model.id))
    screen.addstr('\n')
    screen.refresh()

    # Координаты конца финального и промежуточного результатов
    px = 0; qx = 0
    py = 0; qy = 0

    started = False
    recognized_sentence = "Sentence="

    for result in speech_recognizer.RecognizeSpeech(recognize_from_micro(model_name, block_size_ms)):
        if not started:
            started = True
            py, px = curses.getsyx()
            qy, qx = curses.getsyx()

        part = ""
        for w in result.text.words:
            part += w.text + " "
        is_final = result.is_final

        if is_final:
            recognized_sentence += part

        # Стираем предыдущий промежуточный результат
        erase_text(py, px, qy, qx, screen)

        # Если окно закончилось, добавим несколько пустых строк
        py, qy = add_lines_if_end(py, qy, part, screen)

        if is_final:
            # Добавляем новый финальный
            screen.addstr(py, px, part, curses.color_pair(1))
            screen.refresh()

            # Сохраняем позицию конца финального результата
            py, px = curses.getsyx()
        else:
            # Добавляем новый промежуточный
            screen.addstr(py, px, part, curses.color_pair(0))
            screen.refresh()

            # Сохраняем позицию конца промежуточного результата
            qy, qx = curses.getsyx()

    curses.endwin()

    print("\nRecognized from microphone with model {}:\n{}".format(args.model_name, recognized_sentence))

    with open("result.txt", "w", encoding="utf-8") as f:
        f.write(recognized_sentence)
