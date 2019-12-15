import os
import subprocess
import sys

from .config import CONTAINER_LOGFILE
from .mocker_command import MockerCommand
from .utils import can_chroot, with_logging
from .volume import CONTAINER, Volume, create, copy


class Run(MockerCommand):
    NAME = 'run'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(self.NAME)
        parser.add_argument('image_id', type=int)
        parser.add_argument('command', type=str, nargs='+')
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self, image_id, command):
        image_volume = Volume.get_image(image_id)
        container_volume = create(CONTAINER)
        copy(image_volume, container_volume)

        cmd_file_path = \
            container_volume.path() / CONTAINER.properties["command"]
        cmd_file_path.write_text(" ".join(command) + "\n")

        def preexec():
            os.chdir(str(container_volume.path()))
            os.chroot(str(container_volume.path()))

        log_file_path = container_volume.path() / CONTAINER_LOGFILE

        process = subprocess.Popen(
            command, preexec_fn=preexec, shell=False,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            universal_newlines=True)

        with open(str(log_file_path), 'w') as logfile:
            for line in process.stdout:
                sys.stdout.write(line)
                logfile.write(line)
        process.wait()

    def __call__(self, args):
        if not can_chroot():
            raise PermissionError("chroot requires root privileges")

        image_id = args.image_id
        command = args.command
        self.apply(image_id=image_id, command=command)
