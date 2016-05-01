from .iflist import IFList
import sys


def main():
    ifaces = IFList()
    ifaces.dump(sys.stdout)