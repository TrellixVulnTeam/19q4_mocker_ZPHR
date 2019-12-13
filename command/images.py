from .mocker_command import MockerCommand
from .utils import with_logging


class Images(MockerCommand):
    NAME = 'images'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(self.NAME)
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self):
        raise NotImplementedError()

    def __call__(self, args):
        self.apply()
