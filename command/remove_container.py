from .mocker_command import MockerCommand
from .utils import delete_cgroup, with_logging
from .volume import Volume, delete


class RemoveContainer(MockerCommand):
    NAME = 'rm'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(
            self.NAME, help='remove container and associated namespaces '
                            '(REQUIRES ROOT)')
        parser.add_argument('container_id', type=int,
                            help='id of container to remove')
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self, container_id):
        volume = Volume.get_container(container_id)
        delete_cgroup(container_id)
        delete(volume)

    def __call__(self, args):
        try:
            container_id = args.container_id
            self.apply(container_id=container_id)
        except PermissionError:
            raise PermissionError(
                "root required: removing containers involves changing cgroups")
