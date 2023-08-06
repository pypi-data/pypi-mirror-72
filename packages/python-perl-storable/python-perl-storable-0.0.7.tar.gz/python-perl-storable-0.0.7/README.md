# python_perl_storable

# NAME

python_perl_storable - распаковывает структуру из формата perl-storable

# VERSION

0.0.7

# DESCRIPTION

```python
from python_perl_storable import freeze, thaw

class A:
    def getX(self):
        return self.x

storable_binary_string = freeze({'x': A(x=6), 's': "Здравствуй, Мир!"})

data = thaw(
	storable_binary_string, 
	classes={'A::A': A}, 
	iconv=lambda s: s.decode('windows-1251')
)

print(data) # -> {'x': <__main__.A instance at 0x7f7f532e1050>, 's': "Здравствуй, Мир!"}

print(data['x'].getX()) # -> 6

print(data['s'])        # -> Здравствуй, Мир!
```

# SYNOPSIS

В языке perl есть свой формат бинарных данных для упаковки любых структур: хешей, списков, объектов, регулярок, скаляров, файловых дескрипторов, ссылок, глобов и т.п. Он реализуется модулем https://metacpan.org/pod/Storable.

Данный формат довольно популярен и запакованные в бинарную строку данные различных проектов на perl хранятся во внешних хранилищах: mysql, memcached, tarantool и т.д.

Данный змеиный модуль предназначен для распаковки данных, полученных из таких хранилищ, в структуры python и для упаковки данных питона, чтобы поместить их в хранилище.  

# FUNCTIONS

## thaw

### ARGUMENTS

- storable - бинарная строка
- classes - словарь с классами. Необязательный параметр
- iconv - функция для конвертации строк не в utf8. Необязательный параметр

## freeze

### ARGUMENTS

- data - данные питона: строка, число, словарь, список, объект и т.д.
- magic - булево значение. Необязательно. Добавляет к выводу магическое число 'pst0'

### RETURNS

Бинарная строка с данными в формате Perl Storable

# SCRIPT

```sh
# Заморозить-раморозить:
$ echo '[123, "Хай!"]' | pypls freeze | pypls thaw

# Передавать замороженные данные в бинарном виде:
$ echo '[123, "Хай!"]' | pypls freeze -b | pypls thaw -b

# Передавать код в параметре:
$ pypls freeze --data '[123, "Хай!"]' | pypls thaw

# Добавить магическое число и обесцветить замероженную строку:
$ pypls freeze -m -s --data '[123, "Хай!"]' | pypls thaw

# Перекодировать строки (bytes останутся как есть):
$ pypls freeze --data '[123, "Хай!"]' -i cp1251 | pypls thaw -i cp1251

```

# INSTALL

```sh
$ pip install python-perl-storable
```

# REQUIREMENTS

* data-printer
* argparse

# LICENSE

Copyright (C) Yaroslav O. Kosmina.

This library is free software; you can redistribute it and/or modify
it under the same terms as Python itself.

# AUTHOR

Yaroslav O. Kosmina <darviarush@mail.ru>

# LICENSE

MIT License

Copyright (c) 2020 Yaroslav O. Kosmina

