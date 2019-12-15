from .mocker_command import MockerCommand
from .utils import with_logging
from .volume import Volume, copy


class Commit(MockerCommand):
    NAME = 'commit'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(
            self.NAME, help='apply changes made in container to image')
        parser.add_argument('container_id', type=int,
                            help='id of container containing changes')
        parser.add_argument('image_id', type=int,
                            help='id of image to write changes to')
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self, container_id, image_id):
        container_volume = Volume.get_container(container_id)
        image_volume = Volume.get_image(image_id)
        copy(container_volume, image_volume)

    def __call__(self, args):
        container_id = args.container_id
        image_id = args.image_id
        self.apply(container_id=container_id, image_id=image_id)
