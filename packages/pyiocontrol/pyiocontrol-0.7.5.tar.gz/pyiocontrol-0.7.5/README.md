# pyiocontrol

## Модуль для работы с API iocontrol.ru

Модуль позволяет работать с сервисом iocontrol в интерпретаторе Python версии >= 3

## Установка

__*Вручную:*__

    python3 setup.py install


__*При помощи pip:*__

    pip3 install pyiocontrol

## Примеры:

__*Чтение переменных из панели:*__

``` Python
import pyiocontrol

mypanel = pyiocontrol.Panel("название_панели")

x = mypanel.название_переменной     # например: x = mypanel.mysensor
```

__*Запись переменых в панель:*__

```
import pyiocontrol

mypanel = pyiocontrol.Panel("название_панели")

mypanel.название_переменной = 42    # например: mypanel.mysensor = 42
```
