import contextlib
import os

import cgroups

from ..config import CGROUP_PREFIX


def get_cgroup(container_id):
    cgroup_id = get_cgroup_id(container_id)
    with contextlib.redirect_stderr(open(os.devnull, 'w')):
        return cgroups.Cgroup(cgroup_id)


def create_cgroup(container_id, cpu_limit, memory_limit):
    cgroup = get_cgroup(container_id)
    cgroup.set_cpu_limit(cpu_limit)
    cgroup.set_memory_limit(memory_limit)
    return cgroup


def delete_cgroup(container_id):
    get_cgroup(container_id).delete()


def get_cgroup_id(container_id):
    return CGROUP_PREFIX + str(container_id)
