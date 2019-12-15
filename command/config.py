from pathlib import Path

CONTAINER_LOGFILE = '.log'
VOLUMES_PATH = Path('/var/mocker/volumes')

CGROUP_PREFIX = 'cgroup_'

NETNS_NAMES_PREFIX = 'c'
VETH0_PREFIX = 'veth0_'
VETH1_PREFIX = 'veth1_'
NETNS_PREFIX = 'netns_'
MAC_PREFIX = '02:42:ac:11:00:'
IP_GATEWAY = '10.0.0.1/24'
BRIDGE_INTERFACE_NAME = 'bridge0'
