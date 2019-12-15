import cgroups

from ..config import CGROUP_PREFIX


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
