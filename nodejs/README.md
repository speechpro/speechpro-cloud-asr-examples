Для начала работы создайте аккаунт в [ЦРТ Облака](https://cp.speechpro.com) и получите параметры доступа к API в Личном кабинете.

Перед запуском установите зависимости.

```shell
npm install
```

Установите значение параметров доступа к API в переменные среды
```shell
export SPEECHPRO_USERNAME=username
export SPEECHPRO_DOMAIN_ID=200
export SPEECHPRO_PASSWORD=password
```

### Запуск распознавания из файла с симуляцией реального времени
Звук из файла подается на распознавание порциями по 250мс.
```shell
node file.js {path_to_audio_file}
```

### Запуск распознавания из файла с симуляцией реального времени
Звук с микрофона по умолчанию подается на распознавание в режиме реального времени.
```shell
node microphone.js
```

### Ресурсы
[Документация API распознавания речи](https://asr.cp.speechpro.com/docs)

[Зарегистрироваться в Облаке ЦРТ](https://cp.speechpro.com/home)