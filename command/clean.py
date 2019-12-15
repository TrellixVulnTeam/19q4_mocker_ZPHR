from .config import VOLUMES_PATH
from .mocker_command import MockerCommand
from .utils import with_logging
from .volume import VOLUME_TYPES, delete_volumes


class Clean(MockerCommand):
    NAME = 'clean'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(self.NAME)
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self):
        for type_ in VOLUME_TYPES:
            print("Deleting: " + type_.name)
            delete_volumes(type_)

    def __call__(self, args):
        self.apply()
