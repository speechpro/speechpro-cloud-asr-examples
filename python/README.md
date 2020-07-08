Данный клиент симулирует подачу аудио на распознавание в режиме реального времени порциями по 200мс.

Перед запуском установите зависимости и сгенерируйте код клиента по .proto файлам. Также необходимо заменить параметры аутентификации в API на реальные. Их можно получить в Личном кабинета Облака ЦРТ ([создать аккаунт](https://cp.speechpro.com)).

```shell
pip install -r "requirements.txt"

python -m grpc_tools.protoc -I./protos --python_out=./src --grpc_python_out=./src ./protos/base.proto
python -m grpc_tools.protoc -I./protos --python_out=./src --grpc_python_out=./src ./protos/AsrService.proto
```

### Запуск распознавания из файла с симуляцией реального времени
Звук из файла подается на распознавание порциями по 200мс.
```shell
python src/WavRecognition.py general {path_to_audio_file} --client_id {client_id} --domain_id {domain_id} --api_key {api_key}
```

### Запуск распознавания из файла с симуляцией реального времени
Звук с микрофона по умолчанию подается на распознавание в режиме реального времени и одновременно пишется в файл.
```shell
python src/Microphone.py general --client_id {client_id} --domain_id {domain_id} --api_key {api_key}
```

### Ресурсы
[Документация API распознавания речи](https://asr.cp.speechpro.com/docs)

[Зарегистрироваться в Облаке ЦРТ](https://cp.speechpro.com/home)