GRPC клиент Speechpro Cloud ASR на языке C++.

Параметры аутентификации передаются через аргументы командной строки. Их можно получить в Личном кабинета Облака ЦРТ ([создать аккаунт](https://cp.speechpro.com)).

### Зависимости
```
gRPC::grpc++
```

### Пример сборки
```
mkdir temp_build
cd temp_build
cmake ../ -DCMAKE_PREFIX_PATH=%GRPC_PATH%;%OPENSSL_ROOT_DIR%
cmake --build . --target GRPCExample --config release
```

- GRPC_PATH - расположение установленного grpc
- OPENSSL_ROOT_DIR - расположение установленного openssl

Для запуска grpc и openssl должны быть в переменных окружения или расположены рядом с исполняемым файлом

### Ресурсы
[Документация API распознавания речи](https://asr.cp.speechpro.com/docs)

[Зарегистрироваться в Облаке ЦРТ](https://cp.speechpro.com)

