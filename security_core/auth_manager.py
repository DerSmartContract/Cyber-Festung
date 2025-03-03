import bcrypt
import json
import os
import secrets
import time

USER_DB = "users.json"
RESET_TOKENS = "reset_tokens.json"


class AuthManager:
    def __init__(self):
        self.users = self.load_users()
        self.reset_tokens = self.load_reset_tokens()

    def load_users(self):
        """Lädt Benutzer aus der JSON-Datenbank."""
        if not os.path.exists(USER_DB):
            return {}
        with open(USER_DB, "r") as f:
            return json.load(f)

    def save_users(self):
        """Speichert Benutzer in die JSON-Datenbank."""
        with open(USER_DB, "w") as f:
            json.dump(self.users, f, indent=4)

    def load_reset_tokens(self):
        """Lädt bestehende Reset-Tokens."""
        if not os.path.exists(RESET_TOKENS):
            return {}
        with open(RESET_TOKENS, "r") as f:
            return json.load(f)

    def save_reset_tokens(self):
        """Speichert Reset-Tokens."""
        with open(RESET_TOKENS, "w") as f:
            json.dump(self.reset_tokens, f, indent=4)

    def hash_password(self, password):
        """Hash-Funktion für sichere Passwörter."""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, stored_password, provided_password):
        """Prüft das eingegebene Passwort gegen den Hash."""
        return bcrypt.checkpw(provided_password.encode(), stored_password.encode())

    def register(self, username, password, role="user"):
        """Registriert einen neuen Benutzer."""
        if username in self.users:
            return f"User {username} already exists!"
        self.users[username] = {
            "password": self.hash_password(password),
            "role": role,
            "locked": False,
        }
        self.save_users()
        return f"User {username} registered successfully!"

    def login(self, username, password):
        """Benutzer-Login mit Sperrprüfung."""
        if username not in self.users:
            return "⛔ User not found!"
        if self.users[username]["locked"]:
            return "⛔ Account locked! Reset your password."
        if self.check_password(self.users[username]["password"], password):
            return f"✅ Login successful! Welcome, {username}."
        return "⛔ Invalid password!"

    def generate_reset_token(self, username):
        """Erstellt einen einmaligen Passwort-Reset-Token und speichert ihn."""
        if username not in self.users:
            return "⛔ User not found!"

        token = secrets.token_hex(16)
        self.reset_tokens[username] = {"token": token, "timestamp": time.time()}
        self.save_reset_tokens()

        print(f"🔐 Reset Token für {username}: {token} (Gültig für 10 Min.)")
        return token  # Token zurückgeben

    def reset_password(self, username, token, new_password):
        """Setzt das Passwort zurück, wenn der Token gültig ist."""
        # Lade Tokens neu, um sicherzustellen, dass Änderungen übernommen wurden
        self.reset_tokens = self.load_reset_tokens()

        if username not in self.users:
            return "⛔ User not found!"
        if username not in self.reset_tokens:
            return "⛔ No reset request found!"

        token_data = self.reset_tokens[username]

        # Debugging: Token aus der Datei anzeigen
        print(
            f"📜 Erwarteter Token: {token_data['token']}, Eingereichter Token: {token}"
        )

        # Überprüfen, ob der Token abgelaufen ist
        if time.time() - token_data["timestamp"] > 600:  # 600 Sekunden = 10 Minuten
            del self.reset_tokens[username]
            self.save_reset_tokens()
            return "⛔ Reset token expired!"

        # Überprüfen, ob der Token übereinstimmt
        if token != token_data["token"]:
            return "⛔ Invalid token! Bitte stelle sicher, dass du den richtigen Token verwendest."

        # Neues Passwort setzen und Account entsperren
        self.users[username]["password"] = self.hash_password(new_password)
        self.users[username]["locked"] = False
        del self.reset_tokens[username]  # Token löschen nach Verwendung
        self.save_users()
        self.save_reset_tokens()

        return f"✅ Password for {username} has been successfully reset!"

    def unlock_account(self, admin_user, username):
        """Admin kann gesperrte Nutzer entsperren."""
        if admin_user not in self.users or self.users[admin_user]["role"] not in [
            "admin",
            "super-admin",
        ]:
            return "⛔ Permission denied!"
        if username not in self.users:
            return "⛔ User not found!"

        self.users[username]["locked"] = False
        self.save_users()
        return f"✅ Account {username} has been unlocked!"


if __name__ == "__main__":
    auth = AuthManager()

    # Test-Registrierung
    print(auth.register("testuser", "password123"))

    # Passwort zurücksetzen (Admin ruft diesen Befehl auf)
    reset_token = auth.generate_reset_token("testuser")

    # Test: Token direkt verwenden (richtig eingesetzt!)
    print(auth.reset_password("testuser", reset_token, "newpassword"))

    # Admin entsperrt einen gesperrten Account
    print(auth.unlock_account("admin1", "testuser"))
