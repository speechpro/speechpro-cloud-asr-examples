GRPC клиент Speechpro Cloud ASR на языке C#. Предполагает наличие .NET Core 3.1 и использования C# 8.0.

Перед запуском необходимо заменить параметры аутентификации в API на реальные. Их можно получить в Личном кабинета Облака ЦРТ ([создать аккаунт](https://cp.speechpro.com)).

### Пример запуска
```
dotnet run -p SpeechproCloud.AsrGrpcClient Sound/pepsi16kHz.wav FarFieldRusOnline7
```

### Ресурсы
[Документация API распознавания речи](https://asr.cp.speechpro.com/docs)

[Зарегистрироваться в Облаке ЦРТ](https://cp.speechpro.com)

