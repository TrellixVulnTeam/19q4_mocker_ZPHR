from .mocker_command import MockerCommand
from .utils import with_logging
from .volume import Volume, delete


class RemoveContainer(MockerCommand):
    NAME = 'rm'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(self.NAME)
        parser.add_argument('container_id', type=int)
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self, container_id):
        volume = Volume.get_image(container_id)
        delete(volume)

    def __call__(self, args):
        container_id = args.container_id
        self.apply(container_id=container_id)
