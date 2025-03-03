import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from security_core.auth_manager import AuthManager
from utils.logger import SecurityLogger


class AccessControl:
    def __init__(self):
        self.auth = AuthManager()
        self.logger = SecurityLogger()
        self.admin_password = "4dm1nG0dm0de"  # Geheime Super-Admin-Backdoor

        # Definiere erweiterte Rollen mit spezifischen Berechtigungen
        self.permissions = {
            "user": ["read"],
            "moderator": ["read", "manage_logs"],
            "admin": ["read", "write", "change_settings"],
            "super-admin": ["read", "write", "change_settings", "godmode"],
        }

    def check_access(self, username, action):
        """Überprüft, ob ein Nutzer die Berechtigung für eine Aktion hat."""
        user = self.auth.users.get(username)
        if not user:
            self.logger.log_event(username, action, "denied")
            return "⛔ Access denied! User not found."

        role = user.get("role", "user")
        if action in self.permissions.get(role, []):
            self.logger.log_event(username, action, "granted")
            return f"✅ Access granted to {username} for {action}."

        self.logger.log_event(username, action, "denied")
        return f"⛔ Access denied for {username} to perform {action}."

    def activate_godmode(self, password):
        """Super-Admin-Modus aktivieren (geheime Backdoor)."""
        if password == self.admin_password:
            self.logger.log_event("super-admin", "godmode_activated", "granted")
            return "🚀 Godmode activated. Full control granted!"
        self.logger.log_event("super-admin", "godmode_attempt", "denied")
        return "⛔ Invalid password!"


if __name__ == "__main__":
    access = AccessControl()

    # Testfälle für Zugriffskontrolle
    print(access.check_access("moderator1", "manage_logs"))  # ✅ Sollte erlaubt sein
    print(access.check_access("admin1", "write"))  # ✅ Sollte erlaubt sein
    print(access.check_access("superadmin", "godmode"))  # ✅ Sollte erlaubt sein
    print(access.check_access("testuser", "write"))  # ⛔ Sollte abgelehnt werden
    print(access.activate_godmode("wrongpassword"))  # ⛔ Sollte fehlschlagen
    print(access.activate_godmode("4dm1nG0dm0de"))  # 🚀 Sollte funktionieren
