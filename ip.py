import netaddr
from .mac import MAC


class IP:
    def __init__(self, family, addr, mask=None):
        self.family = family
        self.addr = addr
        self.mask = mask

        if family == 'INET':
            self.version = 4
        elif family == 'INET6':
            self.version = 6
        else:
            self.version = None
            if family == 'LINK':
                self.mac = MAC(self.addr)
                self.is_private = False
                self.is_unicast = not self.mac.multicast
            else:
                self.is_private, self.is_unicast = None, None

        if self.version and mask:
            self.n_ip = netaddr.IPAddress(addr)
            self.n_net = netaddr.IPNetwork('%s/%s' % (addr, mask))

            self.subnet_bits = self.n_net.prefixlen
            self.ip_short = str(self.n_ip)
            self.net_short = str(self.n_net.network)
            self.net_first = netaddr.IPAddress(self.n_net.first)
            self.net_last = netaddr.IPAddress(self.n_net.last)
            self.is_private = self.n_ip.is_private()
            self.is_unicast = self.n_ip.is_unicast()

            if self.version == 4:
                self.ip_long = self.ip_short
            elif self.version == 6:
                self.ip_long = self.n_ip.format(netaddr.ipv6_full)

    @property
    def info(self):
        mac = getattr(self, 'mac')
        if mac:
            return mac.info
        return ' '.join(
            name
            for name in ('multicast', 'reserved',
                         'link_local', 'hostmask',
                         'ipv4_compat', 'ipv4_mapped',
                         'loopback', 'netmask')
            if getattr(self.n_ip, 'is_' + name)())

    def __str__(self):
        ip = getattr(self, 'ip_short', None)
        bits = getattr(self, 'subnet_bits', None)
        if ip and bits:
            return '%s/%d' % (self.ip_short, self.subnet_bits)
        return self.addr
