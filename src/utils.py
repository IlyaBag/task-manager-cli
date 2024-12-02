import csv

from src.entities import StorageState, Task


ID_MAX_BYTES_SIZE = 4


def get_storage_state(path: str) -> StorageState:
    """Read data from storage, transform it into storage state object and
    return that state.
    """

    with open(path, 'r', newline='') as f:
        id_count = int(f.read(ID_MAX_BYTES_SIZE))
        csv_reader = csv.DictReader(f)
        tasks = [Task(**row) for row in csv_reader]
    return StorageState(id_count=id_count, tasks=tasks)


def save_storage_state(path: str, state: StorageState) -> None:
    """Save the received storage state in a storage file."""
    with open(path, 'w', newline='') as f:
        f.write(f'{state['id_count']:0>4}')
        csv_writer = csv.DictWriter(f, fieldnames=Task.get_fields())
        csv_writer.writeheader()
        csv_writer.writerows([task._to_dict() for task in state['tasks']])


def get_id_count(path: str) -> int:
    """Extract an ID counter from storage, convert it to an integer, and
    return it. If the storage file is not found, return -1.
    """

    try:
        with open(path, 'r') as f:
            id_count = int(f.read(ID_MAX_BYTES_SIZE))
    except FileNotFoundError:
        return -1
    return id_count


def save_id_count(path: str, id_count: int) -> None:
    """Save the specified ID counter to the storage."""
    with open(path, 'r+') as f:
        f.seek(ID_MAX_BYTES_SIZE)
        data = f.read()
        f.seek(0)
        f.write(f'{id_count:0>{ID_MAX_BYTES_SIZE}}')
        f.write(data)


def get_id_for_new_task(path: str) -> int:
    """Spawn an id for a new task object creation. Create a new storage file if
    the file specified in 'path' does not exist.
    """

    id_count = get_id_count(path)
    if id_count < 0:
        id_count = init_new_storage(path)
    new_id = id_count + 1
    save_id_count(path, new_id)
    return new_id


def init_new_storage(path: str) -> int:
    """Create a file with an empty storage at the given path and return the
    ID counter.
    """

    empty_state = StorageState(id_count=0, tasks=[])
    save_storage_state(path, empty_state)
    return empty_state['id_count']


def get_task_index_by_id(id: int, tasks: list[Task]) -> int | None:
    """Search task in list of tasks by it's ID."""
    for i, task in enumerate(tasks):
        if task.id == id:
            return i
    return None
