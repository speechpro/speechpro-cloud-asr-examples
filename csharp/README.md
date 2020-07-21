gRPC клиент Speechpro Cloud ASR на языке C#. Предполагает наличие .NET Core 3.1 и использования C# 8.0.

### Распознавание с микрофона

Распознавание аудио с микрофона в реальном времени. Данный пример работает только на Windows в виду использования библиотекой NAudio нативных библиотек для работы с микрофоном.
```shell
dotnet run -p SpeechproCloud.AsrGrpcClient.Microphone general {client_id} {domain_id} {api_key}
```

### Пример распознавание аудио из файла

Перед запуском необходимо заменить параметры аутентификации в API на реальные. Их можно получить в Личном кабинета Облака ЦРТ ([создать аккаунт](https://cp.speechpro.com)). С примере симулируется подача аудио в реальном времени с помощью Thread.Sleep.

```shell
dotnet run -p SpeechproCloud.AsrGrpcClient Sound/pepsi16kHz.wav general
```

### Модели распознавания

|Модель|Описание|
|---|---|
|general|базовая модель для русского языка, работающая в реальном времени|
|general:rc|Release Candidate модели обновления general|

### Ресурсы
[Документация API распознавания речи](https://asr.cp.speechpro.com/docs)

[Зарегистрироваться в Облаке ЦРТ](https://cp.speechpro.com)

