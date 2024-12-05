from src import utils
from src.entities import Task


def get_tasks(path: str) -> str:
    """Show tasks saved in storage. Allow you to filter tasks by category."""

    category = input(
        'Поиск по категории (оставьте поле пустым чтобы показать все задачи): '
    )
    storage = utils.get_storage_state(path)
    if category:
        tasks = [task for task in storage['tasks'] if task.category == category]
    else:
        tasks = storage['tasks']
    return '\n'.join(map(lambda task: str(task), tasks))


def add_task(path: str) -> str:
    """Create a new task and save it to the storage file specified in the 'path'
    parameter. If that path does not exist, it will be created.
    """

    print('Создание новой задачи')
    title = input('[1/5] Название: ')
    description = input('[2/5] Описание: ')
    category = input('[3/5] Категория: ')
    due_date = input('[4/5] Дата окончания срока выполнения задачи в формате '
                     'ГГГГ-ММ-ДД: ')
    while not utils.is_valid_date(due_date):
        due_date = input('Некорректная дата. Введите дату в формате '
                         'ГГГГ-ММ-ДД, например 2024-12-31: ')
    priority = input('[5/5] Приоритет: ')
    status = 'Не выполнена'
    id = utils.get_id_for_new_task(path)

    new_task = Task(
        id=id,
        title=title,
        description=description,
        category=category,
        due_date=due_date,
        priority=priority,
        status=status,
    )

    storage = utils.get_storage_state(path)
    storage['tasks'].append(new_task)
    utils.save_storage_state(path, storage)

    return f'Task created successfully: {new_task}'


def update_task(path: str) -> str:
    """Prompt for the task ID and update the corresponding task with the entered
    values. If the task is not found, display a corresponding message.
    """

    id = int(input('Редактирование задачи. Введите ID задачи, которую '
                   'необходимо изменить: '))
    storage = utils.get_storage_state(path)
    task_index = utils.get_task_index_by_id(id, storage['tasks'])
    if task_index is None:
        return f'Задача с ID = {id} не найдена'

    task = storage['tasks'][task_index]

    print('Введите новое значение поля или пропустите ввод для этого поля.')
    status = input(f'Статус ({task.status}): ')
    if status:
        task.status = status
    else:
        task.title = input(f'[1/5] Название ({task.title}): ') \
            or task.title
        task.description = input(f'[2/5] Описание ({task.description}): ') \
            or task.description
        task.category = input(f'[3/5] Категория ({task.category}): ') \
            or task.category
        task.due_date = input(f'[4/5] Дата окончания ({task.due_date}): ') \
            or task.due_date
        while not utils.is_valid_date(task.due_date):
            task.due_date = input('Некорректная дата. Введите дату в формате '
                            'ГГГГ-ММ-ДД, например 2024-12-31: ')
        task.priority = input(f'[5/5] Приоритет ({task.priority}): ') \
            or task.priority

    utils.save_storage_state(path, storage)

    return f'Task updated successfully: {task}'


def delete_task(path: str) -> str:
    """Prompt for the task ID and delete the corresponding task. If the ID
    prompt was empty, start deleting the category.
    """

    id_input = input('Введите ID задачи, которую необходимо удалить, или '
                     'оставьте поле пустым для удаления категории: ')
    if not id_input:
        deleted = delete_category(path)
        return deleted
    else:
        id = int(id_input)
        storage = utils.get_storage_state(path)
        task_index = utils.get_task_index_by_id(id, storage['tasks'])
        if task_index is None:
            return f'Задача с ID = {id} не найдена'
        deleted_task = storage['tasks'].pop(task_index)
        utils.save_storage_state(path, storage)
        return f'Task deleted successfully: {deleted_task}'


def delete_category(path: str) -> str:
    """Prompt for the task category and delete all corresponding tasks."""

    category = input('Введите название категории, которую необходимо удалить: ')
    storage = utils.get_storage_state(path)
    max_index = len(storage['tasks']) - 1
    for reversed_index, task in enumerate(storage['tasks'][::-1]):
        if task.category == category:
            storage['tasks'].pop(max_index - reversed_index)
    utils.save_storage_state(path, storage)
    return f'Все задачи с категорией "{category}" удалены'


def find_task(path: str) -> str:
    """Promt for a word or words to search for and display tasks containing this
    word/words in the title, description, category or status fields.
    """

    keywords = input('Ключевые слова для поиска: ').lower().split()
    for kw in keywords:
        if not kw.isalnum():
            return ('Ошибка. Все символы должны быть буквами, цифрами '
                    'или пробелами.')
    storage = utils.get_storage_state(path)
    found_tasks = []
    for kw in keywords:
        for task in storage['tasks']:
            if any((kw in task.title.lower(), kw in task.description.lower(),
                    kw in task.category.lower(), kw in task.status.lower())):
                if task not in found_tasks:
                    found_tasks.append(task)
    if not found_tasks:
        return 'Поиск не дал результатов'
    return '\n'.join(map(lambda task: str(task), found_tasks))
