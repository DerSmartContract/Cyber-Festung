import pytest
from security_core.access_control import AccessControl


def test_access_grant(access):
    access.add_role("testuser", "write")
    assert access.check_access("testuser", "write") is True


def test_access_denied(access):
    assert access.check_access("unknown_user", "write") is False


def test_access_wrong_permission(access):
    access.add_role("testuser", "read")
    assert access.check_access("testuser", "write") is False
