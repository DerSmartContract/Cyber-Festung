import sqlite3
import datetime
import time
import os
import subprocess
import socket

LOG_DB = "security_logs.db"
BAN_THRESHOLD = 4  # Anzahl fehlgeschlagener Versuche bis zur Sperre
BAN_DURATION = 300  # Sperrdauer in Sekunden (5 Minuten)


class SecurityMonitor:
    def __init__(self, db_name=LOG_DB):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        """Erstellt die Datenbank-Tabellen, falls sie nicht existieren."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    username TEXT,
                    action TEXT,
                    status TEXT,
                    ip_address TEXT
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS banned_ips (
                    ip_address TEXT PRIMARY KEY,
                    ban_time INTEGER
                )
            """
            )
            conn.commit()

    def log_event(self, username, action, status, ip_address="Unknown"):
        """Speichert ein Ereignis in die Datenbank, inkl. IP-Adresse."""
        timestamp = datetime.datetime.now().isoformat()
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO logs (timestamp, username, action, status, ip_address)
                VALUES (?, ?, ?, ?, ?)
            """,
                (timestamp, username, action, status, ip_address),
            )
            conn.commit()
            print(
                f"📡 [LOG] {timestamp} | User: {username} | Aktion: {action} | Status: {status} | IP: {ip_address}"
            )

    def detect_intrusions(self):
        """Prüft verdächtige Aktivitäten & sperrt IPs, wenn nötig."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT ip_address, COUNT(*) FROM logs
                WHERE status = 'denied' AND timestamp >= datetime('now', '-5 minutes')
                GROUP BY ip_address HAVING COUNT(*) > ?
            """,
                (BAN_THRESHOLD,),
            )
            suspicious_ips = cursor.fetchall()

            for ip, attempts in suspicious_ips:
                print(
                    f"⚠️ ALERT: {ip} hatte {attempts} fehlgeschlagene Login-Versuche in 5 Minuten!"
                )
                self.ban_ip(ip)

    def ban_ip(self, ip_address):
        """Blockiert eine IP-Adresse mit der Firewall."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM banned_ips WHERE ip_address = ?", (ip_address,)
            )
            if cursor.fetchone():
                return  # IP bereits gesperrt

            ban_time = int(time.time()) + BAN_DURATION
            cursor.execute(
                "INSERT INTO banned_ips (ip_address, ban_time) VALUES (?, ?)",
                (ip_address, ban_time),
            )
            conn.commit()

        # MAC OS Firewall Block (pfctl)
        print(f"⛔ Sperre IP: {ip_address}")
        subprocess.run(
            ["sudo", "pfctl", "-t", "blocked", "-T", "add", ip_address], check=False
        )

    def unban_ips(self):
        """Hebt die Sperre für abgelaufene IPs auf."""
        current_time = int(time.time())
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT ip_address FROM banned_ips WHERE ban_time <= ?", (current_time,)
            )
            expired_ips = cursor.fetchall()

            for ip in expired_ips:
                print(f"✅ Entsperre IP: {ip[0]}")
                subprocess.run(
                    ["sudo", "pfctl", "-t", "blocked", "-T", "delete", ip[0]],
                    check=False,
                )
                cursor.execute("DELETE FROM banned_ips WHERE ip_address = ?", (ip[0],))
            conn.commit()

    def live_monitoring(self):
        """Überwacht Logs in Echtzeit und gibt verdächtige Aktivitäten aus."""
        print(
            "🔍 Live-Überwachung mit IP-Sperrung gestartet... (Drücke STRG+C zum Beenden)"
        )
        last_check_time = datetime.datetime.now()

        while True:
            time.sleep(10)  # Alle 10 Sekunden prüfen
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT timestamp, username, action, status, ip_address FROM logs
                    WHERE timestamp >= ?
                    ORDER BY timestamp DESC
                """,
                    (last_check_time.isoformat(),),
                )
                new_logs = cursor.fetchall()

                for log in new_logs:
                    print(f"📡 [{log[0]}] {log[1]} - {log[2]} ({log[3]}) von {log[4]}")

            last_check_time = datetime.datetime.now()
            self.detect_intrusions()
            self.unban_ips()  # Überprüfe, ob gesperrte IPs wieder freigegeben werden können


def get_client_ip():
    """Simuliert das Abrufen einer echten Client-IP."""
    return socket.gethostbyname(socket.gethostname())


if __name__ == "__main__":
    monitor = SecurityMonitor()

    # Test-Logging
    ip_address = get_client_ip()
    monitor.log_event("testuser", "login_attempt", "denied", ip_address)
    monitor.log_event("admin", "login_attempt", "success", ip_address)

    # Live-Monitoring starten
    monitor.live_monitoring()
