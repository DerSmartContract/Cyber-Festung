import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from security_core.auth_manager import AuthManager
from utils.logger import SecurityLogger


class AccessControl:
    def __init__(self, users_file="users.json"):
        self.auth = AuthManager()
        self.logger = SecurityLogger()
        self.users_file = users_file
        self.admin_password = "4dm1nG0dm0de"  # Geheime Super-Admin-Backdoor

        # Definiere erweiterte Rollen mit spezifischen Berechtigungen
        self.permissions = {
            "user": ["read"],
            "moderator": ["read", "manage_logs"],
            "admin": ["read", "write", "change_settings"],
            "super-admin": ["read", "write", "change_settings", "godmode"],
        }

        self.load_users()

    def load_users(self):
        """Lädt die Benutzerliste aus der JSON-Datei."""
        try:
            with open(self.users_file, "r") as file:
                self.users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.users = {}

    def save_users(self):
        """Speichert die Benutzerliste in die JSON-Datei."""
        with open(self.users_file, "w") as file:
            json.dump(self.users, file, indent=4)

    def add_role(self, username, permission):
        """Fügt einem Benutzer eine neue Rolle hinzu."""
        if username in self.users:
            if "permissions" not in self.users[username]:
                self.users[username]["permissions"] = []
            if permission not in self.users[username]["permissions"]:
                self.users[username]["permissions"].append(permission)
                self.save_users()
                return f"✅ Rolle '{permission}' für {username} hinzugefügt!"
        return f"❌ Benutzer {username} nicht gefunden!"

    def check_access(self, username, action):
        """Überprüft, ob ein Nutzer die Berechtigung für eine Aktion hat."""
        user = self.users.get(username)
        if not user:
            self.logger.log_event("ACCESS_DENIED", f"User {username} not found")
            return False  # Fix: Rückgabe als Boolean

        role = user.get("role", "user")
        if action in self.permissions.get(role, []):
            self.logger.log_event("ACCESS_GRANTED", f"{username} -> {action}")
            return True  # Fix: Rückgabe als Boolean

        self.logger.log_event("ACCESS_DENIED", f"{username} denied for {action}")
        return False  # Fix: Rückgabe als Boolean

    def activate_godmode(self, password):
        """Super-Admin-Modus aktivieren (geheime Backdoor)."""
        if password == self.admin_password:
            self.logger.log_event("GODMODE", "Godmode activated!")
            return "🚀 Godmode activated. Full control granted!"
        self.logger.log_event("GODMODE_FAILED", "Invalid godmode attempt")
        return "⛔ Invalid password!"


if __name__ == "__main__":
    access = AccessControl()

    # Testfälle für Zugriffskontrolle
    print(access.add_role("moderator1", "write"))  # ✅ Sollte Rolle hinzufügen
    print(access.check_access("moderator1", "manage_logs"))  # ✅ Sollte True sein
    print(access.check_access("admin1", "write"))  # ✅ Sollte True sein
    print(access.check_access("superadmin", "godmode"))  # ✅ Sollte True sein
    print(access.check_access("testuser", "write"))  # ⛔ Sollte False sein
    print(access.activate_godmode("wrongpassword"))  # ⛔ Sollte fehlschlagen
    print(access.activate_godmode("4dm1nG0dm0de"))  # 🚀 Sollte funktionieren
