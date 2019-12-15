import os
import shlex
import subprocess

from .config import CONTAINER_PIDFILE
from .mocker_command import MockerCommand
from .utils import get_cgroup, can_chroot, with_logging
from .volume import Volume


class ContainerFinishedRunningError(Exception):
    pass


class Execute(MockerCommand):
    NAME = 'exec'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(
            self.NAME, help='enter container and execute command '
                            '(REQUIRES ROOT)')
        parser.add_argument('container_id', type=int,
                            help='id of container to enter')
        parser.add_argument('command', type=str, nargs='+',
                            help='command to execute inside container')
        parser.set_defaults(mocker_command=self)

    @staticmethod
    def _run_process(container_volume, command, preexec):
        container_pid = \
            (container_volume.path() / CONTAINER_PIDFILE).read_text()

        command_str = ' '.join(command)

        command_with_namespaces = \
            'nsenter -t ' + container_pid + ' ' \
            '-m -u -i -n -p ' \
            'chroot ' + str(container_volume.path()) + ' ' \
            + command_str

        process = subprocess.Popen(
            shlex.split(command_with_namespaces),
            preexec_fn=preexec, shell=False, universal_newlines=True)
        process.wait()

    @with_logging
    def apply(self, container_id, command):
        volume = Volume.get_container(container_id)

        if not volume.path().exists():
            raise FileNotFoundError("container does not exist")
        if not (volume.path() / CONTAINER_PIDFILE).exists():
            raise ContainerFinishedRunningError()

        def preexec():
            get_cgroup(container_id).add(os.getpid())

        Execute._run_process(volume, command, preexec)

    def __call__(self, args):
        if not can_chroot():
            raise PermissionError('chroot requires root privileges')

        container_id = args.container_id
        command = args.command
        self.apply(container_id=container_id, command=command)
