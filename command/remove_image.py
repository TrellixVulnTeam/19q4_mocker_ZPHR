from .mocker_command import MockerCommand
from .utils import with_logging


class RemoveImage(MockerCommand):
    NAME = 'rmi'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(self.NAME)
        parser.add_argument('image_id', type=int)
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self, image_id):
        raise NotImplementedError()

    def __call__(self, args):
        image_id = args.image_id
        self.apply(image_id=image_id)