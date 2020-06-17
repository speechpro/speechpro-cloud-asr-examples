GRPC клиент Speechpro Cloud ASR на языке C++.

Параметры аутентификации передаются через аргументы командной строки. Их можно получить в Личном кабинета Облака ЦРТ ([создать аккаунт](https://cp.speechpro.com)).

### Зависимости
```
gRPC::grpc++
```

### Пример сборки
Для сборки также необходимо предварительно сколнировать git submodule. Сделать это можно при помощи следующих команд.
```
git submodule update --init --recursive
```
После этого для сборки выполняем следующие команды.
```
mkdir temp_build
cd temp_build
cmake ../ -DCMAKE_INSTALL_PREFIX=../temp_install
cmake --build . --target GRPCExample --config release
```

Для сборки необходим NASM

### Ресурсы
[Документация API распознавания речи](https://asr.cp.speechpro.com/docs)

[Зарегистрироваться в Облаке ЦРТ](https://cp.speechpro.com)

