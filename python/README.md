Данный клиент симулирует подачу аудио на распознавание в режиме реального времени порциями по 200мс.

Перед запуском установите зависимости.

```shell
pip install -r requirements.txt
```

Запустите программу распознавание речи из файла. Необходимо заменить параметры аутентификации в API на реальные. Их можно получить в Личном кабинета Облака ЦРТ ([создать аккаунт](https://cp.speechpro.com))

```shell
python src/WavRecognition.py FarFieldRusOnline7 //path_to_audio_file --client_id john@doe.com --domain_id 100 --api_key XYZ
```

### Ресурсы
[Документация API распознавания речи](https://asr.cp.speechpro.com/docs)

[Зарегистрироваться в Облаке ЦРТ](https://cp.speechpro.com/home)
