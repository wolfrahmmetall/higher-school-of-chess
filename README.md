# Higher School Of Chess
##### Delivered to you by 4 bishops (2 black, 2 white)

## Запуск сайта
На данный момент сайт запускается локально с помощью нескольких действий
#### Устанавливаем пакеты и зависимости
Переходим в корень проекта
```shell
$ cd path/to/directory/higher-school-of-chess
```
Из файла ```.toml```
```shell
(.venv) $ poetry install
```
Из ```requirements.txt```
```shell
(.venv) $ pip install -r requirements.txt
```
#### Запуск
Сервер
```shell
higher-school-of-chess$ cd backend
higher-school-of-chess/backend$ python -m registration
```
Фронт
```shell
higher-school-of-chess$ cd frontend
higher-school-of-chess/frontend$ npm run dev
```

## Вход и регистрация
#### Вход

<img src="https://i.imghippo.com/files/uc6252vNo.jpg" alt="" border="0">

#### Регистрация

<img src="https://i.imghippo.com/files/nMlu4341Nk.jpg" alt="" border="0">

## Создание и присоединение к играм
Чтобы создать игру, нажмите кнопку ```Создать новую игру```

Чтобы присоединиться к игре, посмотрите на раздел ```Список игр``` и нажмите ```Подключиться к игре``` под интересующей вас игрой

<img src="https://i.imghippo.com/files/NoY8351vMU.jpg" alt="" border="0">

## Настройки игры
Можно настроить время игры в минутах и прибавление после каждого хода (increment) в секундах

<img src="https://i.imghippo.com/files/UjnM7449mSQ.jpg" alt="" border="0">

## Игра
В данной версии, чтобы сделать ход, нужно ввести 2 клетки в шахматной нотации: клетку начала и конца хода в соответствующие поля

Например, ```d2``` и ```d4```

<img src="https://i.imghippo.com/files/JVkz1944FI.jpg" alt="" border="0">
