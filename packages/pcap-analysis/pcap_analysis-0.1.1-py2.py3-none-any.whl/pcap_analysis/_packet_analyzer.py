"""Packet analyzer interface."""

import dpkt

from pcap_analysis._analyzers.arp import Arp
from pcap_analysis._analyzers.bootp import Bootp
from pcap_analysis._analyzers.dhcp import Dhcp
from pcap_analysis._analyzers.icmp import Icmp


class PacketAnalyzer(object):  # pylint: disable=too-few-public-methods

    """Packet analyzer interface.

    :param str pcap_file: path to packet capture file (i.e., `pcap` or`pcapng`)

    """

    def __init__(self, pcap_file):
        self.arp = Arp()
        self.bootp = Bootp()
        self.dhcp = Dhcp()
        self.icmp = Icmp()
        self._analyzers = [  # use instance attribute for make API doc script hook
            self.arp, self.bootp, self.dhcp, self.icmp]

        # Process each packet within each analyzer class instance.
        if pcap_file.endswith(".pcap"):
            reader_class = dpkt.pcap.Reader
        elif pcap_file.endswith(".pcapng"):
            reader_class = dpkt.pcapng.Reader
        else:
            raise ValueError("packet capture must be .pcap or .pcapng format")

        with open(pcap_file, "rb") as pcap_stream:
            pcap_parsed = reader_class(pcap_stream)
            for timestamp, packet_bytes in pcap_parsed:
                ethernet_frame = dpkt.ethernet.Ethernet(packet_bytes)
                for analyzer_ins in self._analyzers:
                    if analyzer_ins._check_packet(ethernet_frame, timestamp=timestamp):
                        analyzer_ins._process_packet(ethernet_frame, timestamp=timestamp)
