import pytest
from threat_detection.honeypot import Honeypot


def test_honeypot_detect_intruder(honeypot):
    honeypot.detect_intruder("192.168.1.99")
    assert len(honeypot.attempts) == 1
    assert honeypot.attempts[0]["ip"] == "192.168.1.99"


def test_honeypot_generate_fake_system(honeypot):
    result = honeypot.generate_fake_system()
    assert result is True
