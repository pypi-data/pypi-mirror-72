import os

import pytest

from pcap_analysis import PacketAnalyzer


class TestIcmp(object):

    @classmethod
    def setup_class(cls):
        capture_file = os.path.join(os.path.dirname(__file__), "icmp_ping.pcapng")
        cls.analyzer = PacketAnalyzer(capture_file)

    @pytest.mark.parametrize("src_ip, target_ip, expected", [
        ("192.168.0.115", "192.168.0.21", True),
        ("192.168.0.115", "192.168.0.100", False),
        ("192.168.0.100", "192.168.0.121", False),
        ("192.168.0.200", "192.168.0.100", False),
    ])
    def test_did_device_ping(self, src_ip, target_ip, expected):
        assert self.analyzer.icmp.did_device_ping(src_ip, target_ip) == expected

    @pytest.mark.parametrize("src_ip, target_ip, expected", [
        ("192.168.0.115", "192.168.0.21", 6),
    ])
    def test_get_ping_count(self, src_ip, target_ip, expected):
        assert self.analyzer.icmp.get_ping_count(src_ip, target_ip) == expected

    @pytest.mark.parametrize("src_ip, target_ip, expected", [
        ("192.168.0.115", "192.168.0.21", 4.3460130692),
    ])
    def test_get_mean_rtt(self, src_ip, target_ip, expected):
        assert round(self.analyzer.icmp.get_mean_rtt(src_ip, target_ip), 10) == expected

    @pytest.mark.parametrize("method_name", [
        "get_ping_count",
        "get_mean_rtt",
    ])
    def test_no_ping_exec(self, method_name):
        with pytest.raises(ValueError) as exec_info:
            getattr(self.analyzer.icmp, method_name)("192.168.0.200", "192.168.0.100")

        assert "host 192.168.0.200 did not ping 192.168.0.100" in str(exec_info.value)
