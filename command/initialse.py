from .mocker_command import MockerCommand
from .utils import with_logging


class Initialise(MockerCommand):
    NAME = 'init'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(self.NAME)
        parser.add_argument('directory', type=str)
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self, directory):
        raise NotImplementedError()

    def __call__(self, args):
        directory = args.directory
        self.apply(directory=directory)
