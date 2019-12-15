from .mocker_command import MockerCommand
from .utils import with_logging
from .volume import Volume, delete


class RemoveImage(MockerCommand):
    NAME = 'rmi'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(
            self.NAME, help='remove image')
        parser.add_argument('image_id', type=int,
                            help='id of image to remove')
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self, image_id):
        volume = Volume.get_image(image_id)
        delete(volume)

    def __call__(self, args):
        image_id = args.image_id
        self.apply(image_id=image_id)
