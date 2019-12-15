import os

import cgroups

from .config import CGROUP_PREFIX


def can_chroot():
    try:
        os.chroot('/')
    except PermissionError:
        return False
    else:
        return True


def create_cgroup(container_id, cpu_limit, memory_limit):
    cgroup_id = get_cgroup_id(container_id)
    cgroup = cgroups.Cgroup(cgroup_id)
    cgroup.set_cpu_limit(cpu_limit)
    cgroup.set_memory_limit(memory_limit)
    return cgroup


def delete_cgroup(container_id):
    cgroup_id = get_cgroup_id(container_id)
    cgroups.Cgroup(cgroup_id).delete()


def get_cgroup_id(container_id):
    return CGROUP_PREFIX + str(container_id)


def with_logging(function):
    def wrapper(self, *args, **kwargs):
        print("mocker.py " + self.NAME + " ", end="")
        print(*[repr(arg) for arg in args], end="")
        print(*["=".join([key, repr(kwargs[key])])
                for key in sorted(kwargs.keys())])
        return function(self, *args, **kwargs)
    return wrapper
