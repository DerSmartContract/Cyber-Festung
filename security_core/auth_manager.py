import bcrypt
import json
import os

USER_DB = "users.json"


class AuthManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists(USER_DB):
            return {}
        with open(USER_DB, "r") as f:
            return json.load(f)

    def save_users(self):
        with open(USER_DB, "w") as f:
            json.dump(self.users, f, indent=4)

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, stored_password, provided_password):
        return bcrypt.checkpw(provided_password.encode(), stored_password.encode())

    def register(self, username, password, role="user"):
        if username in self.users:
            return f"User {username} already exists!"
        self.users[username] = {"password": self.hash_password(password), "role": role}
        self.save_users()
        return f"User {username} registered successfully!"

    def login(self, username, password):
        if username not in self.users:
            return "User not found!"
        if self.check_password(self.users[username]["password"], password):
            return f"Login successful! Welcome, {username}."
        return "Invalid password!"


if __name__ == "__main__":
    auth = AuthManager()
    print(auth.register("admin", "supersecret", "admin"))  # Erster User ist Admin
    print(auth.login("admin", "supersecret"))  # Test-Login
