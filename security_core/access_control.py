from security_core.auth_manager import AuthManager


class AccessControl:
    def __init__(self):
        self.auth = AuthManager()
        self.admin_password = "4dm1nG0dm0de"  # Geheime Backdoor

    def check_access(self, username, action):
        user = self.auth.users.get(username)
        if not user:
            return "Access denied!"

        if user["role"] == "admin" or action == "read":
            return f"Access granted to {username} for {action}."

        return "Access denied!"

    def activate_godmode(self, password):
        if password == self.admin_password:
            return "Godmode activated. Full control granted!"
        return "Invalid password!"


if __name__ == "__main__":
    ac = AccessControl()
    print(ac.check_access("admin", "write"))  # Admin sollte Zugriff haben
    print(ac.activate_godmode("4dm1nG0dm0de"))  # Backdoor testen
