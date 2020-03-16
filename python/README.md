Данный клиент симулирует подачу аудио на распознавание в режиме реального времени порциями по 200мс.

Перед запуском установите зависимости и сгенерируйте код клиента по .proto файлам. Также необходимо заменить параметры аутентификации в API на реальные. Их можно получить в Личном кабинета Облака ЦРТ ([создать аккаунт](https://cp.speechpro.com)).

```python
pip install -r "requirements.txt"

python -m grpc_tools.protoc -I./protos --python_out=./src --grpc_python_out=./src ./protos/base.proto
python -m grpc_tools.protoc -I./protos --python_out=./src --grpc_python_out=./src ./protos/AsrService.proto
```

### Ресурсы
[Документация API распознавания речи](https://asr.cp.speechpro.com/docs)

[Зарегистрироваться в Облаке ЦРТ](https://cp.speechpro.com/home)