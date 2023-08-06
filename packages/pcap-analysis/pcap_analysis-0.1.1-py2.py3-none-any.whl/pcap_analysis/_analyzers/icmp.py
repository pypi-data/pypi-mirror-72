"""Internet control message protocol (ICMP) analyzer."""

from socket import inet_ntoa

import dpkt

from pcap_analysis._analyzers import BaseAnalyzer


class Icmp(BaseAnalyzer):

    """Internet control message protocol (ICMP) analyzer."""

    def __init__(self):
        self._pings = {}  # {source_ip: {target_ip: {seq_num:  {req_ts, resp_ts}, ...}, ...}, ... }

    def _check_packet(self, ethernet_frame, timestamp=None):
        is_icmp_packet = False

        ip_datagram = ethernet_frame.data
        if isinstance(ip_datagram, dpkt.ip.IP):
            icmp_message = ip_datagram.data
            if isinstance(icmp_message, dpkt.icmp.ICMP):
                is_icmp_packet = True

        return is_icmp_packet

    def _process_packet(self, ethernet_frame, timestamp=None):
        ip_datagram = ethernet_frame.data
        icmp_message = ip_datagram.data  # frame unpacking validated in _check_packet method

        if icmp_message.type == dpkt.icmp.ICMP_ECHO:  # ping
            ping_source_host_ip = inet_ntoa(ip_datagram.src)
            ping_target_host_ip = inet_ntoa(ip_datagram.dst)
            ping_seq = int(icmp_message.echo.seq)

            if ping_source_host_ip not in self._pings:
                self._pings[ping_source_host_ip] = {}

            if ping_target_host_ip not in self._pings[ping_source_host_ip]:
                self._pings[ping_source_host_ip][ping_target_host_ip] = {}

            self._pings[ping_source_host_ip][ping_target_host_ip][ping_seq] = {"req_ts": timestamp}

        if icmp_message.type == dpkt.icmp.ICMP_ECHOREPLY:  # ping reply
            ping_source_host_ip = inet_ntoa(ip_datagram.dst)
            ping_target_host_ip = inet_ntoa(ip_datagram.src)
            ping_seq = int(icmp_message.echo.seq)

            try:
                ping_data = self._pings[ping_source_host_ip][ping_target_host_ip][ping_seq]
            except KeyError:
                pass  # unsolicited ping response
            else:
                ping_data["resp_ts"] = timestamp

    def _round_trip_times(self, source_host_ip, target_host_ip):
        if not self.did_device_ping(source_host_ip, target_host_ip):
            raise ValueError("host {0} did not ping {1}".format(source_host_ip, target_host_ip))

        round_trip_times_ms = [
            (req_resp_data["resp_ts"] - req_resp_data["req_ts"]) * 1000
            for _, req_resp_data in self._pings[source_host_ip][target_host_ip].items()]

        return round_trip_times_ms

    def did_device_ping(self, source_host_ip, target_host_ip):
        """Check if the specified source device pinged the specified target IP address.

        :param str source_host_ip: source IP address
        :param str target_host_ip: target IP address
        :returns: device pined specified target
        :rtype: bool

        """
        try:
            pings_by_source = self._pings[source_host_ip]
        except KeyError:
            ping_occurred = False
        else:
            ping_occurred = target_host_ip in pings_by_source

        return ping_occurred

    def get_ping_count(self, source_host_ip, target_host_ip):
        """Count ping requests from source host to target host that received a response.

        :param str source_host_ip: source IP address
        :param str target_host_ip: target IP address
        :returns: number of ping requests with a corresponding response
        :rtype: int

        """
        if not self.did_device_ping(source_host_ip, target_host_ip):
            raise ValueError("host {0} did not ping {1}".format(source_host_ip, target_host_ip))

        pings = len([seq_num for seq_num, req_resp_data in self._pings[source_host_ip][target_host_ip].items()
                     if "resp_ts" in req_resp_data])

        return pings

    def get_mean_rtt(self, source_host_ip, target_host_ip):
        """Calculate average round-trip time for the specified source and target hosts.

        :param str source_host_ip: source IP address
        :param str target_host_ip: target IP address
        :returns: average round-trip time
        :rtype: float

        """
        rtt_list = self._round_trip_times(source_host_ip, target_host_ip)
        return sum(rtt_list) / len(rtt_list)
