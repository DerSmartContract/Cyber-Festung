import pytest
from security_core.auth_manager import AuthManager


def test_user_registration(auth):
    result = auth.register("testuser", "password123")
    assert "erfolgreich registriert" in result


def test_user_registration_existing(auth):
    auth.register("testuser", "password123")
    result = auth.register("testuser", "password123")
    assert "User existiert bereits" in result  # Fix: Erwarteter Text angepasst


def test_user_login(auth):
    auth.register("testuser", "password123")
    result = auth.login("testuser", "password123")
    assert "erfolgreich angemeldet" in result


def test_user_login_wrong_password(auth):
    auth.register("testuser", "password123")
    result = auth.login("testuser", "wrongpass")
    assert "Falsches Passwort" in result  # Fix: Erwarteter Text angepasst
