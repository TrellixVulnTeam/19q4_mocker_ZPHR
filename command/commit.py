from .mocker_command import MockerCommand
from .utils import with_logging


class Commit(MockerCommand):
    NAME = 'commit'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(self.NAME)
        parser.add_argument('container_id', type=int)
        parser.add_argument('image_id', type=int)
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self, container_id, image_id):
        raise NotImplementedError()

    def __call__(self, args):
        container_id = args.container_id
        image_id = args.image_id
        self.apply(container_id=container_id, image_id=image_id)
