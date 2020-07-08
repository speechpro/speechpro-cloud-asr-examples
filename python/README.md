Для начала работы создайте аккаунт в [ЦРТ Облака](https://cp.speechpro.com) и получите параметры доступа к API в Личном кабинете.

Перед запуском установите зависимости.

```shell
pip install -r "requirements.txt"
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
