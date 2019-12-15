import os
import shlex
import subprocess
import sys

from pyroute2 import IPDB, netns

from . import utils
from .config import CONTAINER_LOGFILE, CONTAINER_PIDFILE
from .mocker_command import MockerCommand
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
                            help='command to run inside container'
                                 '(HINT: )')
        parser.add_argument('-c', '--cpu-limit', type=int, default=10,
                            help='CPU shares limit (0-100)')
        parser.add_argument('-m', '--memory-limit', type=int, default=1024,
                            help='Memory limit (MB)')
        parser.set_defaults(mocker_command=self)

    @staticmethod
    def _get_str_command_with_mount(container_volume, command):
        command_str = ' '.join(command)

        if (container_volume.path() / 'bin/sh').exists():
            str_command_with_mount = \
                '/bin/sh -c "/bin/mount -t proc proc /proc && ' \
                + command_str + \
                '"'
        else:
            str_command_with_mount = command_str

        return str_command_with_mount

    @staticmethod
    def _run_process(container_volume, command, preexec):
        str_command_with_mount = Run._get_str_command_with_mount(
            container_volume, command)

        command_with_namespaces = \
            'unshare -f -m -u -i -p --mount-proc ' \
            'chroot ' + str(container_volume.path()) + ' ' \
            + str_command_with_mount

        process = subprocess.Popen(
            shlex.split(command_with_namespaces),
            preexec_fn=preexec, shell=False,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            universal_newlines=True)

        pid = str(process.pid)
        print('Running process with pid: ' + pid + '\n', end='')
        (container_volume.path() / CONTAINER_PIDFILE).write_text(pid)

        log_file_path = container_volume.path() / CONTAINER_LOGFILE
        with open(str(log_file_path), 'w') as logfile:
            for line in process.stdout:
                sys.stdout.write(line)
                logfile.write(line)
        process.wait()

    @utils.with_logging
    def apply(self, image_id, command, cpu_limit, memory_limit):
        image_volume = Volume.get_image(image_id)
        container_volume = create(CONTAINER)
        copy(image_volume, container_volume)

        cmd_file_path = \
            container_volume.path() / CONTAINER.properties['command']
        cmd_file_path.write_text(' '.join(command) + '\n')

        cgroup = utils.create_cgroup(container_volume.id, cpu_limit, memory_limit)

        with IPDB() as ipdb:
            netns_names = utils.create_netns(container_volume.id, ipdb)

            def preexec():
                cgroup.add(os.getpid())
                netns.setns(netns_names.netns)
                os.chdir(str(container_volume.path()))

            try:
                Run._run_process(container_volume, command, preexec)
            finally:
                utils.delete_netns(netns_names, ipdb)

    def __call__(self, args):
        if not utils.can_chroot():
            raise PermissionError('chroot requires root privileges')

        image_id = args.image_id
        command = args.command
        cpu_limit = args.cpu_limit
        memory_limit = args.memory_limit
        self.apply(image_id=image_id, command=command,
                   cpu_limit=cpu_limit, memory_limit=memory_limit)
