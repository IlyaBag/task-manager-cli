from typing import TypedDict


class Task:
    def __init__(self, id: int, title: str, description: str, category: str,
                 due_date: str, priority: str, status: str) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def __str__(self) -> str:
        return (f'[{self.id}] {self.title}. Срок: {self.due_date}. '
                f'Статус: {self.status}.')

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, self.__class__):
            return False
        return all((
            self.id == value.id,
            self.title == value.title,
            self.description == value.description,
            self.category == value.category,
            self.due_date == value.due_date,
            self.priority == value.priority,
            self.status == value.status,
        ))

    def _to_dict(self) -> dict[str, str | int]:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'due_date': self.due_date,
            'priority': self.priority,
            'status': self.status,
        }

    @classmethod
    def get_fields(cls) -> tuple[str, ...]:
        return ('id', 'title', 'description', 'category', 'due_date',
                'priority', 'status')


class StorageState(TypedDict):
    id_count: int
    tasks: list[Task]
