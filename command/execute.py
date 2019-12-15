from .mocker_command import MockerCommand
from .utils import with_logging


class Execute(MockerCommand):
    NAME = 'exec'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(
            self.NAME, help='enter container and execute command')
        parser.add_argument('container_id', type=int,
                            help='id of container to enter')
        parser.add_argument('command', type=str, nargs='+',
                            help='command to execute inside container')
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self, container_id, command):
        raise NotImplementedError()

    def __call__(self, args):
        container_id = args.container_id
        command = args.command
        self.apply(container_id=container_id, command=command)
