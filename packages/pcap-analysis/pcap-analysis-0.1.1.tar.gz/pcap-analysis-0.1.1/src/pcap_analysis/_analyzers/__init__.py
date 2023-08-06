"""Base packet analyzer class."""

BROADCAST_IP = "255.255.255.255"
BROADCAST_MAC = "ff:ff:ff:ff:ff:ff"
NULL_IP = "0.0.0.0"
NULL_MAC = "00:00:00:00:00:00"


class BaseAnalyzer(object):  # pylint: disable=too-few-public-methods

    """Base packet analyzer class."""

    def _check_packet(self, ethernet_frame, timestamp=None):  # pragma: no cover
        raise NotImplementedError("packet analyzer plug-in does not implement _check_packet")

    def _process_packet(self, ethernet_frame, timestamp=None):  # pragma: no cover
        raise NotImplementedError("packet analyzer plug-in does not implement _process_packet")
