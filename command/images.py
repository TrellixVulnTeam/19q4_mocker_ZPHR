from .mocker_command import MockerCommand
from .utils import with_logging
from .volume import IMAGE, list_volumes


class Images(MockerCommand):
    NAME = 'images'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(self.NAME)
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self):
        list_volumes(IMAGE)

    def __call__(self, args):
        self.apply()
