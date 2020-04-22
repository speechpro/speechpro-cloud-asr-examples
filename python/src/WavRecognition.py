import grpc
from google.protobuf import empty_pb2

import base_pb2
import AsrService_pb2
import AsrService_pb2_grpc

import os
import time
import numpy as np
import soundfile as sf
import samplerate as sr
import argparse
import colorama
from termcolor import cprint


def recognize_wav(model_name, wav_filename):
    """Генератор запросов на распознавание"""
    # Конфигурируем распознавание на модель model_name
    yield AsrService_pb2.RecognizeRequest(config=AsrService_pb2.RecognitionConfig(
        auth=AsrService_pb2.Auth(
            client_id='',
            domain_id='',
            api_key=''
        ),
        model=base_pb2.Model(id=model_name)))

    model_samplerate = 16000

    # Cчитываем wav-файл кусочками по 1 секунде
    with sf.SoundFile(wav_filename, mode='r') as wav:
        wav_samplerate = wav.samplerate
        samples_to_read = int(wav_samplerate / 5)

        # Настройки для передискретизации звука
        # Converter type:
        # sinc_best = 0, sinc_medium = 1, sinc_fastest = 2, zero_order_hold = 3, linear = 4
        # Описание типов: http://www.mega-nerd.com/libsamplerate/api_misc.html

        resampler = sr.Resampler(converter_type="sinc_best")
        resampling_ratio = float(model_samplerate) / wav_samplerate
        print("resampling_ratio: {}\n".format(resampling_ratio))

        while wav.tell() < wav.frames:
            wave_data = wav.read(samples_to_read, dtype="int16")
            sound_for_recognition = wave_data

            # Запускаем передискрет только, если частота модели и файла не совпадают
            if resampling_ratio != 1.0:
                resampled_data = resampler.process(
                    wave_data, resampling_ratio, end_of_input=(wav.tell() >= wav.frames)).astype(np.int16)
                sound_for_recognition = resampled_data

            # Отправляем звук на распознавание
            yield AsrService_pb2.RecognizeRequest(
                sound=AsrService_pb2.Sound(samples=sound_for_recognition.tobytes()))

            time.sleep(0.2)

    # Завершаем распознавание
    yield AsrService_pb2.RecognizeRequest(finish=base_pb2.Finish())


def protobuf_punct_mark_2_text(punct):
    proto_enum_punct_2_text = {
        "NONE": "",
        "DOT": ".",
        "COMMA": ",",
        "COLON": ":",
        "SEMICOLON": ";",
        "EXCLAMATION_POINT": "!",
        "QUESTION_MARK": "?",
        "DASH": "-",
        "SPEAKER_CHANGE": ".-"
    }
    return proto_enum_punct_2_text[base_pb2._WORD_PUNCTUATIONMARK.values_by_number[punct].name]


def recognize_file(model_name, filename):
    file_extension = os.path.splitext(filename)[1]
    recognized_sentence = "Sentence="
    color1 = "green"
    color2 = "white"

    for result in speech_recognizer.RecognizeSpeech(recognize_wav(model_name, filename)):
        part = ""
        for w in result.text.words:
            part += w.text + " "

        if result.is_final:
            recognized_sentence += part + protobuf_punct_mark_2_text(w.punctuation_mark)
            cprint(part, color1)
        else:
            cprint(part, color2)

    print("\nRecognized file {} with model {}:\n{}".format(filename, args.model_name, recognized_sentence))

    # Пишем результат в файл
    with open("result.txt", 'w', encoding='utf-8') as f:
        f.write(recognized_sentence)


if __name__ == '__main__':
    # Командые аргументы
    parser = argparse.ArgumentParser()
    parser.add_argument("model_name", type=str, help="Model ID for recognition")
    parser.add_argument("input", type=str, help="input (directory or file)")
    args = parser.parse_args()

    # Соединяемся с сервером
    creds = grpc.ssl_channel_credentials()
    channel = grpc.secure_channel('asr.cp.speechpro.com', creds)

    # Будем использовать сервис распознавания речи
    speech_recognizer = AsrService_pb2_grpc.SpeechRecognitionStub(channel)

    model_list = speech_recognizer.GetListOfSpeechRecognitionModels(
        AsrService_pb2.Auth(
            client_id='',
            domain_id='',
            api_key=''
        ))
    print("All available speech recognition models:")
    for model in model_list.models:
        print(model.id)
    print('')


    # Инициализация цвета в консоли
    colorama.init()

    if os.path.isdir(args.input):
        for root, dirs, files in os.walk(args.input):
            for file in files:
                recognize_file(args.model_name, os.path.join(root, file))
    else:
        if os.path.isfile(args.input):
            recognize_file(args.model_name, args.input)
        else:
            print("{}: no such file or directory".format(args.input))
