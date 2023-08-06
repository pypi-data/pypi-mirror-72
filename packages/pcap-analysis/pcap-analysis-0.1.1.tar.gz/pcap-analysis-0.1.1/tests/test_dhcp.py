import os

from pcap_analysis import PacketAnalyzer


class TestDhcp(object):

    @classmethod
    def setup_class(cls):
        dhcp_capture_file = os.path.join(os.path.dirname(__file__), "dhcp.pcap")
        cls.analyzer = PacketAnalyzer(dhcp_capture_file)

    def test_did_client_make_request(self):
        assert self.analyzer.dhcp.did_client_make_request("00:0b:82:01:fc:42")
        assert not self.analyzer.dhcp.did_client_make_request("18:90:3f:7a:56:a4")

    def test_did_client_receive_ip_address(self):
        assert self.analyzer.dhcp.did_client_receive_ip_address("00:0b:82:01:fc:42")
        assert not self.analyzer.dhcp.did_client_receive_ip_address("18:90:3f:7a:56:a4")

    def test_get_received_ip_address(self):
        assert self.analyzer.dhcp.get_received_ip_address("00:0b:82:01:fc:42") == "192.168.0.10"
