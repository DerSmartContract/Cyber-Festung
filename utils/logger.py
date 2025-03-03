import sqlite3
import datetime


class SecurityLogger:
    def __init__(self, db_name="security_logs.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    username TEXT,
                    action TEXT,
                    status TEXT
                )
            """
            )

    def log_event(self, username, action, status="success"):
        timestamp = datetime.datetime.now().isoformat()
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO logs (timestamp, username, action, status)
                VALUES (?, ?, ?, ?)
            """,
                (timestamp, username, action, status),
            )

    def fetch_logs(self):
        with self.conn:
            return self.conn.execute("SELECT * FROM logs").fetchall()


if __name__ == "__main__":
    logger = SecurityLogger()
    logger.log_event("admin", "login_attempt")
    print(logger.fetch_logs())
