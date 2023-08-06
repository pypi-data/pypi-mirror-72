"""Bootstrap protocol (BOOTP) analyzer."""

import dpkt

from pcap_analysis._analyzers import BaseAnalyzer
from pcap_analysis._dpkt_cnv import unpack_ip_addr, unpack_mac_addr


class Bootp(BaseAnalyzer):

    """Bootstrap protocol (BOOTP) analyzer."""

    _mac_address_states = {}
    _assigned_ip_addresses = {}

    def _check_packet(self, ethernet_frame, timestamp=None):
        is_bootp_packet = False

        ip_datagram = ethernet_frame.data
        if isinstance(ip_datagram, dpkt.ip.IP):
            udp_segment = ip_datagram.data
            if isinstance(udp_segment, dpkt.udp.UDP):
                try:
                    bootp_message = dpkt.dhcp.DHCP(udp_segment.data)
                except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
                    pass
                else:
                    # Verify packet contains DHCP magic cookie and message type option.
                    if bootp_message.magic != dpkt.dhcp.DHCP_MAGIC:
                        is_bootp_packet = True

                    contains_dhcp_message = False
                    for option, _ in bootp_message.opts:
                        if option == dpkt.dhcp.DHCP_OPT_MSGTYPE:
                            contains_dhcp_message = True

                    # Some observed BOOTP servers still use DHCP magic cookie even in BOOTP mode.
                    # Therefore, consider packet to be BOOTP is the message type option isn't present.
                    if not contains_dhcp_message:
                        is_bootp_packet = True

        return is_bootp_packet

    def _process_packet(self, ethernet_frame, timestamp=None):
        bootp_message = dpkt.dhcp.DHCP(ethernet_frame.data.data.data)  # frame unpacking validated above
        bootp_message_type = int(bootp_message.op)
        client_mac_str = unpack_mac_addr(bootp_message.chaddr)

        if bootp_message_type == dpkt.dhcp.DHCP_OP_REQUEST:
            self._mac_address_states[client_mac_str] = dpkt.dhcp.DHCP_OP_REQUEST

        if bootp_message_type == dpkt.dhcp.DHCP_OP_REPLY:
            try:
                previous_state = self._mac_address_states[client_mac_str]
            except KeyError:
                pass
            else:
                if previous_state == dpkt.dhcp.DHCP_OP_REQUEST:
                    self._mac_address_states[client_mac_str] = dpkt.dhcp.DHCP_OP_REPLY
                    self._assigned_ip_addresses[client_mac_str] = unpack_ip_addr(bootp_message.yiaddr)

    def did_client_make_request(self, mac_address):
        """Check if a device requested an IP address using BOOTP.

        :param str mac_address: client device MAC address
        :returns: client made BOOTP request
        :rtype: bool

        """
        return mac_address.lower() in self._mac_address_states

    def did_client_receive_ip_address(self, mac_address):
        """Check if a device received an IP address using BOOTP.

        :param str mac_address: client device MAC address
        :returns: client received IP address
        :rtype: bool

        """
        return mac_address.lower() in self._assigned_ip_addresses

    def get_received_ip_address(self, mac_address):
        """Get IP address assigned to device via BOOTP.

        :param str mac_address: client device MAC address
        :returns: assigned IP address
        :rtype: str
        :raises ValueError: no IP address assigned to specified MAC address

        """
        standardized_mac_address = mac_address.lower()
        if standardized_mac_address not in self._assigned_ip_addresses:
            raise ValueError("no IP address obtained by MAC address" + standardized_mac_address)

        return self._assigned_ip_addresses[standardized_mac_address]
