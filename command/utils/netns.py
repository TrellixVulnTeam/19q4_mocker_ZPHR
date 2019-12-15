from pyroute2 import IPDB, NetNS, netns

from .. import config


class NetNSNames:
    def __init__(self, container_id):
        container_name = config.NETNS_NAMES_PREFIX + str(container_id)
        self.veth0 = config.VETH0_PREFIX + container_name
        self.veth1 = config.VETH1_PREFIX + container_name
        self.mac = self.get_mac(container_id)
        self.ip = self.get_ip(container_id)
        self.netns = config.NETNS_PREFIX + container_name

    @staticmethod
    def get_mac(id_):
        return config.MAC_PREFIX + str(hex(id_)).split('x')[1].rjust(2, '0')

    @staticmethod
    def get_ip(id_):
        ip, mask = config.IP_GATEWAY.split('/')
        ip_parts = ip.split('.')
        ip_parts[-1] = str(id_)
        return '/'.join(['.'.join(ip_parts), mask])


def create_netns(container_id, ipdb):
    netns_names = NetNSNames(container_id)
    setup_interface(netns_names, ipdb)
    setup_netns(netns_names, ipdb)
    return netns_names


def setup_interface(netns_names, ipdb):
    existing_interfaces = ipdb.interfaces.keys()
    if config.BRIDGE_INTERFACE_NAME not in existing_interfaces:
        ipdb.create(
            kind='bridge', ifname=config.BRIDGE_INTERFACE_NAME
        ).commit()

    with ipdb.create(
            kind='veth', ifname=netns_names.veth0, peer=netns_names.veth1
    ) as interface:
        interface.up()
        interface.set_target('master', config.BRIDGE_INTERFACE_NAME)


def setup_netns(netns_names, ipdb):
    netns.create(netns_names.netns)

    with ipdb.interfaces[netns_names.veth1] as veth1:
        veth1.net_ns_fd = netns_names.netns

    ns = IPDB(nl=NetNS(netns_names.netns))

    with ns.interfaces.lo as lo:
        lo.up()

    with ns.interfaces[netns_names.veth1] as veth1:
        veth1.address = netns_names.mac
        veth1.add_ip(netns_names.ip)
        veth1.up()

    ns.routes.add({
        'dst': 'default',
        'gateway': config.IP_GATEWAY.split('/')[0]
    }).commit()


def delete_netns(netns_names, ipdb):
    NetNS(netns_names.netns).close()
    netns.remove(netns_names.netns)
    ipdb.interfaces[netns_names.veth0].remove()
