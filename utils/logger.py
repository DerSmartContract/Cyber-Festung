import sqlite3
import time

LOG_DB = "security_logs.db"


class SecurityLogger:
    def __init__(self, db_file=LOG_DB):
        self.db_file = db_file
        self._init_db()

    def _init_db(self):
        """Erstellt oder aktualisiert die Log-Datenbank mit allen benötigten Spalten."""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    username TEXT NOT NULL,
                    action TEXT NOT NULL,
                    status TEXT NOT NULL,
                    ip_address TEXT NOT NULL
                )
            """
            )
            conn.commit()

    def log_event(self, username, action, status, ip_address="Unknown"):
        """Speichert ein Sicherheitsereignis in der Datenbank."""
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO logs (timestamp, username, action, status, ip_address) VALUES (?, ?, ?, ?, ?)",
                (timestamp, username, action, status, ip_address),
            )
            conn.commit()

    def get_logs(self, limit=10):
        """Holt die letzten Logs."""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM logs ORDER BY id DESC LIMIT ?", (limit,))
            return cursor.fetchall()


# Datenbank aktualisieren, falls Datei direkt ausgeführt wird
if __name__ == "__main__":
    logger = SecurityLogger()
    print("✅ Logs-Datenbank erfolgreich aktualisiert!")
