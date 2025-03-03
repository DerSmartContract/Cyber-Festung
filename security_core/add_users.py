import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from security_core.auth_manager import AuthManager


auth = AuthManager()

# Fehlende Benutzer registrieren
print(auth.register("moderator1", "modpassword", "moderator"))
print(auth.register("admin1", "adminpass", "admin"))
print(auth.register("superadmin", "superpass", "super-admin"))

# Speichern der Änderungen
auth.save_users()

print("✅ Alle neuen Benutzer wurden erfolgreich hinzugefügt!")
