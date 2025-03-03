import pytest
from security_core.auth_manager import AuthManager
from security_core.access_control import AccessControl
from threat_detection.honeypot import Honeypot


@pytest.fixture
def auth():
    return AuthManager()


@pytest.fixture
def access():
    return AccessControl()


@pytest.fixture
def honeypot():
    return Honeypot()
