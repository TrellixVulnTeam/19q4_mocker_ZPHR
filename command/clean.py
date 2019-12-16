from .mocker_command import MockerCommand
from .remove_image import RemoveImage
from .remove_container import RemoveContainer
from .utils import with_logging
from .volume import IMAGE, CONTAINER, VOLUMES_PATH


class Clean(MockerCommand):
    NAME = 'clean'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(
            self.NAME, help='run rmi,rm on all images,containers (MAY REQUIRE ROOT)')
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self):
        removers = {
            IMAGE: RemoveImage(),
            CONTAINER: RemoveContainer(),
        }

        for type_, remover in removers.items():
            for volume_path in VOLUMES_PATH.iterdir():
                name = volume_path.name
                if not name.startswith(type_.prefix):
                    continue

                id_ = name[len(type_.prefix):]
                remover.apply(int(id_))

    def __call__(self, args):
        self.apply()
