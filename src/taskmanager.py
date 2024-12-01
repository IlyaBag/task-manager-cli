import argparse

from src import crud


def main() -> None:
    """The main entry point to the application. Processes arguments passed by
    the user via the command line and calls the appropriate action function.
    """

    actions = {'get': crud.get_tasks,
               'add': crud.add_task,
               'update': crud.update_task,
               'delete': crud.delete_task,
               'find': crud.find_task}
    action_names = [act for act in actions]

    parser = argparse.ArgumentParser(
        description='TaskManager allows you to manage your tasks',
    )
    parser.add_argument(
        'action',
        choices=action_names,
        help=f'Select one of the available actions: {', '.join(action_names)}',
        metavar='action',
    )
    parser.add_argument('-f', '--file', default='tasks.csv', help='Set path to storage file. Defaults to "tasks.csv"')
    args = parser.parse_args()

    actions[args.action](args.file)


if __name__ == '__main__':
    main()
