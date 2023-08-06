"""Convenience functions for dpkt package."""

import struct
from socket import inet_ntoa

from dpkt.compat import compat_ord


def unpack_ip_addr(hex_addr):
    """Unpack integer form IP address.

    :param int hex_addr: IP address in single-integer form
    :rtype: dotted decimal IP address
    :rtype: str

    """
    return inet_ntoa(struct.pack(">L", hex_addr))


def unpack_mac_addr(hex_addr):
    """Unpack MAC address from bytes representation.

    :param bytes hex_addr: MAC address bytes
    :returns: MAC address with colon-delimited octets
    :rtype: str

    """
    return ':'.join('%02x' % compat_ord(b) for b in hex_addr)
