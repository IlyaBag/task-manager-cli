import argparse


def main() -> None:
    """The main entry point to the application. Processes arguments passed by
    the user via the command line and calls the appropriate action function.
    """

    actions = {'get': get_tasks,
               'add': add_task,
               'update': update_task,
               'delete': delete_task,
               'find': find_task}
    action_names = [act for act in actions]

    parser = argparse.ArgumentParser(
        description='TaskManager - manager for your tasks',
    )
    parser.add_argument(
        'action',
        choices=action_names,
        help=f'Select one of the available actions: {', '.join(action_names)}',
        metavar='action',
    )
    args = parser.parse_args()

    actions[args.action]()

def get_tasks() -> None:
    print('All tasks')

def add_task() -> None:
    print('Task added')

def update_task() -> None:
    print('Task updated')

def delete_task() -> None:
    print('Task deleted')

def find_task() -> None:
    print('Task finded')


if __name__ == '__main__':
    main()
