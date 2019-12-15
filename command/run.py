import os
import subprocess
import sys

from .config import CONTAINER_LOGFILE
from .mocker_command import MockerCommand
from .utils import can_chroot, create_cgroup, with_logging
from .volume import CONTAINER, Volume, create, copy


class Run(MockerCommand):
    NAME = 'run'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(
            self.NAME, help='run command in isolated container based on image '
                            '(REQUIRES ROOT)')
        parser.add_argument('image_id', type=int,
                            help='image to use for container')
        parser.add_argument('command', type=str, nargs='+',
                            help='command to run inside container')
        parser.add_argument('-c', '--cpu-limit', type=int, default=10,
                            help='CPU shares limit (0-100)')
        parser.add_argument('-m', '--memory-limit', type=int, default=1024,
                            help='Memory limit (MB)')
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self, image_id, command, cpu_limit, memory_limit):
        image_volume = Volume.get_image(image_id)
        container_volume = create(CONTAINER)
        copy(image_volume, container_volume)

        cmd_file_path = \
            container_volume.path() / CONTAINER.properties['command']
        cmd_file_path.write_text(' '.join(command) + '\n')

        cgroup = create_cgroup(container_volume.id, cpu_limit, memory_limit)

        def preexec():
            cgroup.add(os.getpid())
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
            raise PermissionError('chroot requires root privileges')

        image_id = args.image_id
        command = args.command
        cpu_limit = args.cpu_limit
        memory_limit = args.memory_limit
        self.apply(image_id=image_id, command=command,
                   cpu_limit=cpu_limit, memory_limit=memory_limit)
