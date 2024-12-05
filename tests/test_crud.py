import sys
from src import crud, utils
from src.entities import Task


def test_get_tasks(create_test_storage):
    test_storage_path = create_test_storage
    crud.input = lambda _: ''
    all_tasks = crud.get_tasks(test_storage_path)
    expected_result = (
        '[1] Изучить основы FastAPI. Категория: Обучение. Срок: 2024-11-30. Статус: Не выполнена.\n'
        '[2] Изучить основы Django. Категория: Обучение. Срок: 2024-07-20. Статус: Не выполнена.\n'
        '[3] Сварить суп. Категория: Кулинария. Срок: 2024-11-22. Статус: Выполнена.'
    )
    assert all_tasks == expected_result


def test_get_tasks_with_category(create_test_storage):
    test_storage_path = create_test_storage
    crud.input = lambda _: 'Обучение'
    all_tasks = crud.get_tasks(test_storage_path)
    expected_result = (
        '[1] Изучить основы FastAPI. Категория: Обучение. Срок: 2024-11-30. Статус: Не выполнена.\n'
        '[2] Изучить основы Django. Категория: Обучение. Срок: 2024-07-20. Статус: Не выполнена.'
    )
    assert all_tasks == expected_result


def test_add_task(create_test_storage):
    test_storage_path = create_test_storage
    test_task_fields = (
        'TestTask',
        'TestDescription',
        'TestCategory',
        '2222-11-11',
        'TestPriority',
    )
    test_task_inputer = (field for field in test_task_fields)
    crud.input = lambda _: next(test_task_inputer)

    result = crud.add_task(test_storage_path)
    assert result == 'Task created successfully: [4] TestTask. Категория: TestCategory. Срок: 2222-11-11. Статус: Не выполнена.'

    with open(test_storage_path, 'r') as f:
        lines = f.readlines()
    expected_line = '4,TestTask,TestDescription,TestCategory,2222-11-11,TestPriority,Не выполнена\n'
    assert lines[-1] == expected_line, f'Result line = {expected_line}'


def test_update_task(create_test_storage):
    test_storage_path = create_test_storage
    updated_task_fields = (
        '3',  # input task id
        '',  # input task status
        '',  # input task title
        'Нужно срочно приготовить обед',  # input task description
        '',  # input task category
        '',  # input task due_date
        'Высокий',  # input task priority
    )
    test_task_inputer = (field for field in updated_task_fields)
    crud.input = lambda _: next(test_task_inputer)

    result = crud.update_task(test_storage_path)
    assert result == 'Task updated successfully: [3] Сварить суп. Категория: Кулинария. Срок: 2024-11-22. Статус: Выполнена.'

    with open(test_storage_path, 'r') as f:
        lines = f.readlines()
    expected_line = '3,Сварить суп,Нужно срочно приготовить обед,Кулинария,2024-11-22,Высокий,Выполнена\n'
    assert lines[-1] == expected_line, f'Result line = {expected_line}'


def test_update_task_status(create_test_storage):
    test_storage_path = create_test_storage
    updated_task_fields = (
        '3',  # input task id
        'Не выполнена',  # input task status
    )
    test_task_inputer = (field for field in updated_task_fields)
    crud.input = lambda _: next(test_task_inputer)

    result = crud.update_task(test_storage_path)
    assert result == 'Task updated successfully: [3] Сварить суп. Категория: Кулинария. Срок: 2024-11-22. Статус: Не выполнена.'

    with open(test_storage_path, 'r') as f:
        lines = f.readlines()
    expected_line = '3,Сварить суп,Нужно приготовить обед,Кулинария,2024-11-22,Обычный,Не выполнена\n'
    assert lines[-1] == expected_line, f'Result line = {expected_line}'


def test_delete_task(create_test_storage):
    test_storage_path = create_test_storage
    crud.input = lambda _: '3'

    result = crud.delete_task(test_storage_path)
    assert result == 'Task deleted successfully: [3] Сварить суп. Категория: Кулинария. Срок: 2024-11-22. Статус: Выполнена.'

    with open(test_storage_path, 'r') as f:
        lines = f.readlines()
    expected_line ='2,Изучить основы Django,Пройти документацию по Django и создать простой проект,Обучение,2024-07-20,Высокий,Не выполнена\n'
    assert lines[-1] == expected_line, f'Result line = {expected_line}'


def test_delete_category(create_test_storage):
    test_storage_path = create_test_storage
    crud.input = lambda _: 'Обучение'

    result = crud.delete_category(test_storage_path)
    assert result == 'Все задачи с категорией "Обучение" удалены'

    with open(test_storage_path, 'r') as f:
        lines = f.read()

    expected_line = (
        '0003id,title,description,category,due_date,priority,status\n'
        '3,Сварить суп,Нужно приготовить обед,Кулинария,2024-11-22,Обычный,Выполнена\n'
    )
    assert lines == expected_line, f'Result line = {expected_line}'


def test_find_task(create_test_storage):
    test_storage_path = create_test_storage
    crud.input = lambda _: 'основы документацию'

    result = crud.find_task(test_storage_path)
    expected_result = (
        '[1] Изучить основы FastAPI. Категория: Обучение. Срок: 2024-11-30. Статус: Не выполнена.\n'
        '[2] Изучить основы Django. Категория: Обучение. Срок: 2024-07-20. Статус: Не выполнена.'
    )
    assert result == expected_result


def test_find_task_negative_case(create_test_storage):
    test_storage_path = create_test_storage
    crud.input = lambda _: 'ошибки'

    result = crud.find_task(test_storage_path)
    expected_result = 'Поиск не дал результатов'
    assert result == expected_result


def test_find_task_invalid_input(create_test_storage):
    test_storage_path = create_test_storage
    crud.input = lambda _: 'два, слова'

    result = crud.find_task(test_storage_path)
    expected_result =('Ошибка. Все символы должны быть буквами, цифрами '
                      'или пробелами.')
    assert result == expected_result
