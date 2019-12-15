from .mocker_command import MockerCommand
from .utils import with_logging


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
        raise NotImplementedError()

    def __call__(self, args):
        image = args.image
        self.apply(image=image)
