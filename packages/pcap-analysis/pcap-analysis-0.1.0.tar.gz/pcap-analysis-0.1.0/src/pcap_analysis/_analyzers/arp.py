"""Address resolution protocol (ARP) analyzer."""

from socket import inet_ntoa

import dpkt

from pcap_analysis._analyzers import BaseAnalyzer, BROADCAST_MAC, NULL_IP, NULL_MAC
from pcap_analysis._dpkt_cnv import unpack_mac_addr


class Arp(BaseAnalyzer):

    """Address resolution protocol (ARP) analyzer."""

    _device_arp_tables = {}  # does not include gratuitous ARPs -- they are added in dynamically later
    _gratuitous_announcements = {}
    _mac_address_states = {}  # keyed by (sender MAC, query target IP)
    _probes = {}

    def _check_packet(self, ethernet_frame, timestamp=None):
        is_arp_packet = False

        arp_message = ethernet_frame.data
        if isinstance(arp_message, dpkt.arp.ARP):
            is_arp_packet = True

        return is_arp_packet

    def _ensure_table_exists_for_mac(self, mac_address):
        if mac_address not in self._device_arp_tables and mac_address not in [BROADCAST_MAC, NULL_MAC]:
            self._device_arp_tables[mac_address] = {}

    def _process_packet(self, ethernet_frame, timestamp=None):
        dst_eth_mac = unpack_mac_addr(ethernet_frame.dst)

        arp_message = ethernet_frame.data  # ARP message unpacking validated above
        src_arp_mac = unpack_mac_addr(arp_message.sha)
        dst_arp_mac = unpack_mac_addr(arp_message.tha)
        src_arp_ip = inet_ntoa(arp_message.spa)
        dst_arp_ip = inet_ntoa(arp_message.tpa)

        self._ensure_table_exists_for_mac(src_arp_mac)
        self._ensure_table_exists_for_mac(dst_arp_mac)

        if src_arp_ip == dst_arp_ip and dst_eth_mac == BROADCAST_MAC:  # is gratuitous
            if src_arp_mac not in self._gratuitous_announcements:
                self._gratuitous_announcements[src_arp_mac] = []

            self._gratuitous_announcements[src_arp_mac].append(src_arp_ip)
        elif src_arp_ip == NULL_IP and dst_eth_mac == BROADCAST_MAC:  # probe
            if src_arp_mac not in self._probes:
                self._probes[src_arp_mac] = []

            self._probes[src_arp_mac].append(dst_arp_ip)
        else:
            if arp_message.op == dpkt.arp.ARP_OP_REQUEST:
                self._mac_address_states[(src_arp_mac, dst_arp_ip)] = dpkt.arp.ARP_OP_REQUEST

            if arp_message.op == dpkt.arp.ARP_OP_REPLY:
                try:
                    previous_state = self._mac_address_states[(dst_arp_mac, src_arp_ip)]
                except KeyError:
                    pass
                else:
                    if previous_state == dpkt.arp.ARP_OP_REQUEST:
                        self._mac_address_states[(dst_arp_mac, src_arp_ip)] = dpkt.arp.ARP_OP_REPLY
                        self._device_arp_tables[
                            dst_arp_mac][src_arp_ip] = src_arp_mac

    def did_device_arp_for(self, mac_address, target_ip):
        """Check if the specified device ARPed for the specified target IP address.

        :param str mac_address: device MAC address
        :param str target_ip: target IP address
        :returns: device sent ARP packet(s)
        :rtype: bool

        """
        return (mac_address.lower(), target_ip) in self._mac_address_states

    def did_device_receive_response(self, mac_address, target_ip):
        """Check if the specified device received an ARP reply from the specified target IP address.

        If the device received a response, the IP and MAC address are included in the ARP table accessible with the
        ``get_arp_table`` method.

        :param str mac_address: device MAC address
        :param str target_ip: target IP address
        :returns: device received ARP reply
        :rtype: bool

        """
        return target_ip in self.get_arp_table(mac_address, include_gratuitous=False)

    def get_arp_table(self, mac_address, include_gratuitous=True):
        """Generate a hypothetical ARP table based on network traffic.

        :param str mac_address: device MAC address
        :param bool include_gratuitous: include gratuitous ARP entries
        :returns: generated ARP table
        :rtype: dict
        :raises ValueError: specified MAC address not observed in network traffic

        """
        mac_address = mac_address.lower()

        try:
            arp_table = self._device_arp_tables[mac_address]
        except KeyError:
            raise ValueError("MAC address {0} not observed in network traffic".format(mac_address))
        else:
            arp_table = arp_table.copy()

        if include_gratuitous:
            for gratuitous_mac, announced_ip_addresses in self._gratuitous_announcements.items():
                most_recent_ip = announced_ip_addresses[-1]
                arp_table[most_recent_ip] = gratuitous_mac

        return arp_table

    def get_gratuitous_arp_ips(self, mac_address):
        """Get set of IP address(es) announced via gratuitous ARP for the specified device.

        :param str mac_address: device MAC address
        :returns: announced IP addresses
        :rtype: set of str
        :raises ValueError: no gratuitous ARP packets sent from specified MAC address

        """
        standardized_mac_address = mac_address.lower()
        if standardized_mac_address not in self._gratuitous_announcements:
            raise ValueError("no gratuitous ARP sent by MAC address" + standardized_mac_address)

        return set(self._gratuitous_announcements[standardized_mac_address])

    def get_probed_ips(self, mac_address):
        """Get set of IP address(es) probed by the specified device.

        :param str mac_address: device MAC address
        :returns: probed IP addresses
        :rtype: set of str
        :raises ValueError: no probe ARP packets sent from specified MAC address

        """
        standardized_mac_address = mac_address.lower()
        if standardized_mac_address not in self._gratuitous_announcements:
            raise ValueError("no probe ARP sent by MAC address" + standardized_mac_address)

        return set(self._gratuitous_announcements[standardized_mac_address])
