from .config import CONTAINER_LOGFILE
from .mocker_command import MockerCommand
from .utils import with_logging
from .volume import Volume


class Logs(MockerCommand):
    NAME = 'logs'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(
            self.NAME, help='print container logs')
        parser.add_argument('container_id', type=int,
                            help='id of container to print logs of')
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self, container_id):
        volume = Volume.get_container(container_id)
        logfile = volume.path() / CONTAINER_LOGFILE
        print(logfile.read_text())

    def __call__(self, args):
        container_id = args.container_id
        self.apply(container_id=container_id)
