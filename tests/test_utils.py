from src.entities import StorageState
from src import utils


def test_get_storage_state(create_test_storage, create_test_tasks):
    task1, task2, task3 = create_test_tasks
    expected_state = StorageState(id_count=3, tasks=[task1, task2, task3])
    state = utils.get_storage_state(create_test_storage)
    assert state == expected_state


def test_save_storage_state(create_test_storage, create_test_tasks):
    task1, task2, task3 = create_test_tasks
    task1.status = 'Выполнена'
    task2.priority = 'Обычный'
    new_state = StorageState(id_count=3, tasks=[task1, task2, task3])

    path = create_test_storage
    utils.save_storage_state(path, new_state)

    expected_data = (
        '0003id,title,description,category,due_date,priority,status\n'
        '1,Изучить основы FastAPI,Пройти документацию по FastAPI и создать простой проект,Обучение,2024-11-30,Высокий,Выполнена\n'
        '2,Изучить основы Django,Пройти документацию по Django и создать простой проект,Обучение,2024-07-20,Обычный,Не выполнена\n'
        '3,Сварить суп,Нужно приготовить обед,Кулинария,2024-11-22,Обычный,Выполнена\n'
    )
    with open(path, 'r') as f:
        saved_state = f.read()
    assert saved_state == expected_data


def test_get_id_count(create_test_storage):
    expected_id_count = 3
    test_file_path = create_test_storage
    id_count = utils.get_id_count(test_file_path)
    assert id_count == expected_id_count


def test_save_id_count(create_test_storage):
    path = create_test_storage
    id_count = 12
    utils.save_id_count(path, id_count)
    with open(path, 'r') as f:
        saved_id_count = int(f.read(utils.ID_MAX_BYTES_SIZE))
        other_data = f.read()
    assert saved_id_count == id_count, \
        f'Expected value = {id_count}, saved value = {saved_id_count}'
    assert other_data, 'All tasks were lost'
