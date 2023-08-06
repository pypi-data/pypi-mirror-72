import os

from pcap_analysis import PacketAnalyzer


class TestBootp(object):

    @classmethod
    def setup_class(cls):
        bootp_capture_file = os.path.join(os.path.dirname(__file__), "bootp.pcapng")
        cls.analyzer = PacketAnalyzer(bootp_capture_file)

    def test_did_client_make_request(self):
        assert not self.analyzer.bootp.did_client_make_request("00:0b:82:01:fc:42")
        assert self.analyzer.bootp.did_client_make_request("18:90:3f:7a:56:a4")

    def test_did_client_receive_ip_address(self):
        assert not self.analyzer.bootp.did_client_receive_ip_address("00:0b:82:01:fc:42")
        assert self.analyzer.bootp.did_client_receive_ip_address("18:90:3f:7a:56:a4")

    def test_get_received_ip_address(self):
        assert self.analyzer.bootp.get_received_ip_address("18:90:3f:7a:56:a4") == "192.168.1.5"
