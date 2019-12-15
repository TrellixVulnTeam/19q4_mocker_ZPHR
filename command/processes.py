from .mocker_command import MockerCommand
from .utils import with_logging
from .volume import CONTAINER, list_volumes


class Processes(MockerCommand):
    NAME = 'ps'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(
            self.NAME, help='list all container volumes')
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self):
        list_volumes(CONTAINER)

    def __call__(self, args):
        self.apply()
