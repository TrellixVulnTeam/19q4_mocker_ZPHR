from distutils.dir_util import copy_tree
from pathlib import Path

from .mocker_command import MockerCommand
from .utils import with_logging
from .volume import IMAGE, create


class Initialise(MockerCommand):
    NAME = 'init'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(
            self.NAME, help='create image from directory')
        parser.add_argument('directory', type=str,
                            help='directory for image base')
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self, directory):
        path = Path(directory)
        if not path.exists():
            raise FileNotFoundError(path)
        if not path.is_dir():
            raise NotADirectoryError(path)
        path = path.resolve()

        volume = create(IMAGE)

        copy_tree(str(path), str(volume.path()))

        source_file = volume.path() / IMAGE.properties['source']
        source_file.write_text(str(path) + '\n')

    def __call__(self, args):
        directory = args.directory
        self.apply(directory=directory)
