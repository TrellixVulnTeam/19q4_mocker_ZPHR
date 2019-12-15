from .mocker_command import MockerCommand
from .utils import download_image_from_dockerhub, with_logging
from .volume import IMAGE, create


class Pull(MockerCommand):
    NAME = 'pull'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(
            self.NAME, help='create image from dockerhub image (latest)')
        parser.add_argument('image', type=str,
                            help='name of dockerhub image')
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self, image):
        volume = create(IMAGE)
        download_image_from_dockerhub(image, volume.path())

    def __call__(self, args):
        image = args.image
        self.apply(image=image)
