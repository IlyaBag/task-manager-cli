# Тестовое задание для Hitalent

## Описание

Приложение представляет собой CLI утилиту для управления задачами (TaskManager)
и предоставляет стандартный набор CRUD-операций для работы со списком задач.
Задачи хранятся в виде csv-файла.

### Используемые сущности

#### Task
  - `id`: int
  - `title`: str - заголовок задачи
  - `description`: str - описание задачи
  - `category`: str - категория задачи
  - `due_date`: str - срок исполнения задачи в формате ISO (ГГГГ-ММ-ДД)
  - `priority`: str - приоритет задачи
  - `status`: str - текущий статус задачи

#### StorageState(TypedDict)
  - `id_count`: int - счётчик выданных id
  - `tasks`: list[Task] - список задач

### Структура хранилища

Задачи хранятся в стандартном csv-файле с одной особенностью - в первой строке
файла перед названиями полей записывается счетчик выданных id `id_count`.
Счетчик представляет собой строку из цифр с лидирующими нулями. По умолчанию
под счетчик отводится 4 байта, но этот размер можно установить вручную изменив
в файле _utils.py_ константу `ID_MAX_BYTES_SIZE`.

Этот нюанс хранения данных стоит учитывать при самостоятельной обработке файла
хранилища.

## Управление

Чтобы воспользоваться приложением, нужно запустить в командной строке
python-модуль `src.taskmanager` с указанием следующих аргументов:

- `action` - __обязательный__ аргумент, задающий действие, которое пользователь
хочет выполнить
- `-f` или `--file` - опциональный параметр, позволяющий указать путь до файла
хранилища задач (по умолчанию имеет значение `tasks.csv`)
- `-h` или `--help` - показывает справку по использованию приложения

Параметр `action` может принимать 5 значений:

- `get` - посмотреть все задачи или задачи с определённой категорией
- `add` - создать новую задачу
- `update` - изменить статус определённой задачи или отредактировать задачу
- `delete` - удалить определённую задачу или категорию задач
- `find` - поиск задач по ключевым словам

## Основные зависимости

Проект написан с использованием Python 3.12 и не требует для запуска установки
дополнительных зависимостей.

В разработке использовались следующие библиотеки:

- pytest 8.3.3
- flake8 7.1.1

## Установка приложения

Приложение не требует установки. Достаточно клонировать репозиторий командой

```
git clone https://github.com/IlyaBag/task-manager-cli.git
```

## Запуск приложения

Для запуска приложения нужно перейти в директорию, в которую склонирован
репозиторий, и запустить python-скрипт с соответствующими аргументами.

После запуска приложение в интерактивном режиме запросит необходимые параметры и
выполнит требуемое действие. Если файл, указанный в аргументе `--file`, не
существует, то он будет создан автоматически.

### Пример запуска приложения:

```
cd task-manager-cli
python3 -m src.taskmanager add --file my_tasks.csv
```

Удачи в использовании!
