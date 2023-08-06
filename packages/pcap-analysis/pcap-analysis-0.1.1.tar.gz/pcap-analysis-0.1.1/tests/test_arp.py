import os

import pytest

from pcap_analysis import PacketAnalyzer


class TestArp(object):

    @classmethod
    def setup_class(cls):
        capture_file = os.path.join(os.path.dirname(__file__), "arp.pcapng")
        cls.analyzer = PacketAnalyzer(capture_file)

    @pytest.mark.parametrize("mac, ip, expected", [
        ("9e:d9:72:28:0e:7b", "192.168.1.36", True),
        ("9E:D9:72:28:0E:7B", "192.168.1.36", True),  # uppercase variety
        ("9E:D9:72:28:0E:7B", "192.168.1.2", False),
        ("1A:2B:3C:4D:5E:6F", "192.168.1.2", False),
    ])
    def test_did_device_arp_for(self, mac, ip, expected):
        assert self.analyzer.arp.did_device_arp_for(mac, ip) == expected

    @pytest.mark.parametrize("mac, ip, expected", [
        ("9e:d9:72:28:0e:7b", "192.168.1.5", True),
        ("9e:d9:72:28:0e:7b", "192.168.1.36", False),
    ])
    def test_did_device_receive_response(self, mac, ip, expected):
        assert self.analyzer.arp.did_device_receive_response(mac, ip) == expected

    @pytest.mark.parametrize("mac, include_gratuitous, table", [
        ("9e:d9:72:28:0e:7b", False, {"192.168.1.5": "9f:77:b7:df:d9:d4"}),
        ("89:4a:14:94:38:15", False, {}),
        ("9e:d9:72:28:0e:7b", True, {
            "192.168.1.5": "9f:77:b7:df:d9:d4", "192.168.1.41": "89:4a:14:94:38:15",
            "192.168.1.90": "d1:72:59:de:2d:c5"}),
        ("89:4a:14:94:38:15", True, {
            "192.168.1.41": "89:4a:14:94:38:15", "192.168.1.90": "d1:72:59:de:2d:c5",
            "192.168.1.5": "9f:77:b7:df:d9:d4"}),
    ])
    def test_get_arp_table(self, mac, include_gratuitous, table):
        assert self.analyzer.arp.get_arp_table(mac, include_gratuitous=include_gratuitous) == table

    @pytest.mark.parametrize("mac, ips", [
        ("89:4a:14:94:38:15", {"192.168.1.41"}),
        ("d1:72:59:de:2d:c5", {"192.168.1.90"}),
    ])
    def test_get_gratuitous_arp_ips(self, mac, ips):
        assert self.analyzer.arp.get_gratuitous_arp_ips(mac) == ips

    @pytest.mark.parametrize("mac, ips", [
        ("89:4a:14:94:38:15", {"192.168.1.41"}),
        ("d1:72:59:de:2d:c5", {"192.168.1.90"}),
        ("9f:77:b7:df:d9:d4", {"192.168.1.5"}),
    ])
    def test_get_probed_ips(self, mac, ips):
        assert self.analyzer.arp.get_probed_ips(mac) == ips
