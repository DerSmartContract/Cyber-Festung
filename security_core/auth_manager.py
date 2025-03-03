import json
import bcrypt
import sqlite3
import time
from utils.logger import SecurityLogger

LOG_DB = "security_logs.db"


class AuthManager:
    def __init__(self, users_file="users.json"):
        self.users_file = users_file
        self.logger = SecurityLogger()
        self.load_users()
        self._init_log_db()

    def load_users(self):
        """Lädt die Benutzer aus der JSON-Datei."""
        try:
            with open(self.users_file, "r") as file:
                self.users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.users = {}

    def save_users(self):
        """Speichert die Benutzer in die JSON-Datei."""
        with open(self.users_file, "w") as file:
            json.dump(self.users, file, indent=4)

    def register(self, username, password, role="user"):
        """Registriert einen neuen Benutzer mit gehashtem Passwort."""
        if username in self.users:
            return "❌ User existiert bereits!"

        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        self.users[username] = {"password": hashed_pw, "role": role, "locked": False}
        self.save_users()

        self.logger.log_event(username, "register", "success", "N/A")
        return "✅ User erfolgreich registriert!"

    def login(self, username, password):
        """Überprüft Login-Daten eines Benutzers und speichert das Ereignis."""
        if username not in self.users:
            self.logger.log_event(username, "login_attempt", "denied", "Unknown")
            return "⛔ User nicht gefunden!"

        stored_password = self.users[username]["password"]
        if bcrypt.checkpw(password.encode(), stored_password.encode()):
            self.logger.log_event(username, "login_attempt", "granted", "Unknown")
            return "✅ User erfolgreich angemeldet!"

        self.logger.log_event(username, "login_attempt", "denied", "Unknown")
        return "⛔ Falsches Passwort!"

    def _init_log_db(self):
        """Erstellt die `logs`-Tabelle in SQLite, falls sie nicht existiert."""
        self.logger._init_db()


# Falls Datei direkt ausgeführt wird
if __name__ == "__main__":
    auth = AuthManager()
    print(auth.register("testuser", "password123"))
    print(auth.login("testuser", "password123"))
    print(auth.login("testuser", "wrongpassword"))
    print(auth.login("unknownuser", "password"))
    print(auth.users)