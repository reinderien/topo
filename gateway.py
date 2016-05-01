from .ip import IP


class Gateway:
    def __init__(self, family, addr, iface, is_default):
        self.family = family
        self.ip = IP(family, addr)
        self.iface = iface
        self.is_default = is_default

    def __str__(self):
        return self.ip.ip_short