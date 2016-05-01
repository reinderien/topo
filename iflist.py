import netifaces
from .gateway import Gateway
from .ip import IP


class IFList:
    def __init__(self):
        all_gateways = netifaces.gateways()

        self.default_gateways = {}
        for f, ads in all_gateways['default'].items():
            family = self._family_title(f)
            self.default_gateways[family] = Gateway(family, *ads, is_default=True)

        self.gateways = {}
        for f, ads in all_gateways.items():
            if f != 'default':
                family = self._family_title(f)
                self.gateways[family] = [Gateway(family, *ad) for ad in ads]

        self.addrs = {iface: {self._family_title(a): ads
                              for a, ads in netifaces.ifaddresses(iface).items()}
                      for iface in netifaces.interfaces()}

        for iface, families in self.addrs.items():
            for family, ads in families.items():
                new_ads = [IP(family, d.get('addr'), mask=d.get('netmask'))
                           for d in ads]
                ads.clear()
                ads.extend(new_ads)

    @staticmethod
    def _family_title(n):
        return netifaces.address_families[n].lstrip('AF_')

    def dump(self, out):
        out.write('Gateways:\n')
        g_line = '%7s %6s %20s %7s\n'
        out.write(g_line % ('iface', 'family', 'addr', 'default'))
        for gateway in (gateway
                        for gateways in self.gateways.values()
                        for gateway in gateways):
            out.write(g_line % (gateway.iface,
                                gateway.family,
                                gateway.ip,
                                gateway.is_default))
        out.write('\n')

        out.write('Addresses:\n')
        a_line = '%7s %6s %40s %25s %3s %7s %7s %s\n'
        out.write(a_line % ('iface', 'family', 'addr',
                            'net', '/', 'private', 'unicast', 'info'))
        for iface, families in self.addrs.items():
            for family, ads in families.items():
                for ip in ads:
                    out.write(a_line % (
                        iface, family, ip.addr,
                        getattr(ip, 'net_short', ''),
                        getattr(ip, 'subnet_bits', ''),
                        '*' if ip.is_private else '',
                        '*' if ip.is_unicast else '',
                        getattr(ip, 'info', '')))
