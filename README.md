# hh_parcer_mtuci
Репозиторий для учебной ознакомительной практики в МТУСИ: Парсер платформы hh.ru

# Описание файлов.
**main.py** - основная программа, которая запускает телеграмм бота в качестве интерфейса для ввода параметров для парсинга платформы hh.ru. \
**api_hh.py** - модуль, реализующий отправку HTTP запросов к сайту api.hh.ru . \
**db_helper.py** - модуль, реалзиующий работу с базой данной PostgreSQL, а также за вывод отработанных команд /search и /analytics. \
**SQL_code** - модуль, хранящий SQL скрипты, для работы модуля db_helper. \
**connection_db_constant.py** - модуль хранящий константы, для подключения к базе данных. \
**hh_table CREATE script.sql** - SQL скрипт для создания таблицы, для записи результатов парсинга по запросу из telegram бота. \
**hh_parcing_id_seq.sql** - SQL sequence для таблицы hh_table. \
**telegram_bot_table CREATE script.sql** - SQL скрипт для создания таблицы, для записи информации о telegram пользователе, а также содержание запроса пользователя. \
**telegram_table_id_seq.sql** - SQL sequence для таблицы telegram_table. \
# Для запуска программы необходимо:
1) Развернуть DockerFile с помощью docker-compose.
2) В случае отсутствия Docker Desktop, для работы программы необоходимо установить:

Python 3.12
Библиотека pyTelegramBotAPI(или же telebot)
Библиотека psycopg2

После чего необходимо в консоль ввести команду: python main.py

