"""Dynamic host configuration protocol (DHCP) analyzer."""

import dpkt

from pcap_analysis._analyzers import BaseAnalyzer
from pcap_analysis._dpkt_cnv import unpack_ip_addr, unpack_mac_addr


class Dhcp(BaseAnalyzer):

    """Dynamic host configuration protocol (DHCP) analyzer."""

    def __init__(self):
        self._mac_address_states = {}
        self._assigned_ip_addresses = {}

    def _check_packet(self, ethernet_frame, timestamp=None):
        is_dhcp_packet = False

        ip_datagram = ethernet_frame.data
        if isinstance(ip_datagram, dpkt.ip.IP):  # pylint: disable=too-many-nested-blocks
            udp_segment = ip_datagram.data
            if isinstance(udp_segment, dpkt.udp.UDP):
                try:
                    dhcp_message = dpkt.dhcp.DHCP(udp_segment.data)
                except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
                    pass
                else:
                    # Verify packet contains DHCP magic cookie and message type option.
                    if dhcp_message.magic == dpkt.dhcp.DHCP_MAGIC:
                        for option, _ in dhcp_message.opts:
                            if option == dpkt.dhcp.DHCP_OPT_MSGTYPE:
                                is_dhcp_packet = True

        return is_dhcp_packet

    def _process_packet(self, ethernet_frame, timestamp=None):  # pylint: disable=too-many-branches
        dhcp_message = dpkt.dhcp.DHCP(ethernet_frame.data.data.data)  # frame unpacking validated above
        client_mac_str = unpack_mac_addr(dhcp_message.chaddr)

        dhcp_message_type = None
        for option, value in dhcp_message.opts:
            if option == dpkt.dhcp.DHCP_OPT_MSGTYPE:
                dhcp_message_type = ord(value)

        assert dhcp_message_type

        if dhcp_message_type == dpkt.dhcp.DHCPDISCOVER:
            self._mac_address_states[client_mac_str] = dpkt.dhcp.DHCPDISCOVER

        if dhcp_message_type == dpkt.dhcp.DHCPOFFER:
            try:
                previous_state = self._mac_address_states[client_mac_str]
            except KeyError:
                pass
            else:
                if previous_state == dpkt.dhcp.DHCPDISCOVER:
                    self._mac_address_states[client_mac_str] = dpkt.dhcp.DHCPOFFER

        if dhcp_message_type == dpkt.dhcp.DHCPREQUEST:
            try:
                previous_state = self._mac_address_states[client_mac_str]
            except KeyError:
                pass
            else:
                if previous_state == dpkt.dhcp.DHCPOFFER:
                    self._mac_address_states[client_mac_str] = dpkt.dhcp.DHCPREQUEST

        if dhcp_message_type == dpkt.dhcp.DHCPACK:
            try:
                previous_state = self._mac_address_states[client_mac_str]
            except KeyError:
                pass
            else:
                if previous_state == dpkt.dhcp.DHCPREQUEST:
                    self._mac_address_states[client_mac_str] = dpkt.dhcp.DHCPACK
                    self._assigned_ip_addresses[client_mac_str] = unpack_ip_addr(dhcp_message.yiaddr)

    def did_client_make_request(self, mac_address):
        """Check if a device requested an IP address using DHCP.

        :param str mac_address: client device MAC address
        :returns: client made DHCP request
        :rtype: bool

        """
        return mac_address.lower() in self._mac_address_states

    def did_client_receive_ip_address(self, mac_address):
        """Check if a device received an IP address using DHCP.

        :param str mac_address: client device MAC address
        :returns: client received IP address
        :rtype: bool

        """
        return mac_address.lower() in self._assigned_ip_addresses

    def get_received_ip_address(self, mac_address):
        """Get IP address assigned to device via DHCP.

        :param str mac_address: client device MAC address
        :returns: assigned IP address
        :rtype: str
        :raises ValueError: no IP address assigned to specified MAC address

        """
        standardized_mac_address = mac_address.lower()
        if standardized_mac_address not in self._assigned_ip_addresses:
            raise ValueError("no IP address obtained by MAC address " + standardized_mac_address)

        return self._assigned_ip_addresses[standardized_mac_address]
