import netaddr
from netaddr.core import NotRegisteredError


class MAC:
    def __init__(self, addr):
        self.addr = addr
        self.eui = netaddr.EUI(addr)
        self.multicast = bool(self.eui.packed[0] & 1)
        self.local = bool(self.eui.packed[0] & 2)

    @property
    def info(self):
        s = 'ver={ver}{multic}{local}{iab}'.format(
                multic=' multicast' if self.multicast else '',
                local=' local' if self.local else ' universal',
                iab=' iab' if self.eui.is_iab() else '',
                ver=self.eui.version)
        try:
            org = self.eui.info['OUI']['org']
            s += ' org=%s' % org
        except NotRegisteredError:
            pass
        return s
