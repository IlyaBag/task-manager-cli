import os
import sys
sys.path.insert(1, os.path.dirname(sys.path[0]))

from typing import Generator

import pytest

from src.entities import Task


PATH_TO_TEST_FILE = 'test_tasks.csv'


@pytest.fixture
def create_test_storage() -> Generator[str, None, None]:
    """Create a test storage file and yield the path to this file. Delete the
    created file after the test is completed.
    """

    test_data = [
        '0003id,title,description,category,due_date,priority,status\n',
        '1,Изучить основы FastAPI,Пройти документацию по FastAPI и создать простой проект,Обучение,2024-11-30,Высокий,Не выполнена\n',
        '2,Изучить основы Django,Пройти документацию по Django и создать простой проект,Обучение,2024-07-20,Высокий,Не выполнена\n',
        '3,Сварить суп,Нужно приготовить обед,Кулинария,2024-11-22,Обычный,Выполнена\n',
    ]
    with open(PATH_TO_TEST_FILE, 'w') as f:
        f.writelines(test_data)
    yield PATH_TO_TEST_FILE
    os.remove(PATH_TO_TEST_FILE)

@pytest.fixture
def create_test_tasks() -> tuple[Task, Task]:
    """Create three different Task objects."""
    task1 = Task(
        id=1,
        title='Изучить основы FastAPI',
        description='Пройти документацию по FastAPI и создать простой проект',
        category='Обучение',
        due_date='2024-11-30',
        priority='Высокий',
        status='Не выполнена'
    )
    task2 = Task(
        id=2,
        title='Изучить основы Django',
        description='Пройти документацию по Django и создать простой проект',
        category='Обучение',
        due_date='2024-07-20',
        priority='Высокий',
        status='Не выполнена'
    )
    task3 = Task(
        id=3,
        title='Сварить суп',
        description='Нужно приготовить обед',
        category='Кулинария',
        due_date='2024-11-22',
        priority='Обычный',
        status='Выполнена'
    )
    return task1, task2, task3
