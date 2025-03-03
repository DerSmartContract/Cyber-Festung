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

    def detect_intrusions(self):
        """Prüft verdächtige Aktivitäten & sperrt IPs, wenn nötig."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT ip_address, COUNT(*) FROM logs
                WHERE status = 'denied' 
                AND timestamp >= datetime('now', '-5 minutes')
                GROUP BY ip_address 
                HAVING COUNT(*) >= ?
            """,
                (BAN_THRESHOLD,),
            )
            suspicious_ips = cursor.fetchall()

            if suspicious_ips:
                for row in suspicious_ips:
                    ip = row[0]
                    attempts = row[1]
                    print(
                        f"⚠️ ALERT: {ip} hatte {attempts} fehlgeschlagene Login-Versuche in 5 Minuten!"
                    )
                    self.ban_ip(ip)
            else:
                print("✅ Keine verdächtigen Aktivitäten erkannt.")

    def ban_ip(self, ip_address):
        """Blockiert eine IP-Adresse mit der Firewall."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM banned_ips WHERE ip_address = ?", (ip_address,)
            )
            if cursor.fetchone():
                print(f"⛔ {ip_address} ist bereits gesperrt.")
                return  # IP bereits gesperrt

            ban_time = int(time.time()) + BAN_DURATION
            cursor.execute(
                "INSERT INTO banned_ips (ip_address, ban_time) VALUES (?, ?)",
                (ip_address, ban_time),
            )
            conn.commit()

        print(f"⛔ Sperre IP: {ip_address}")
        subprocess.run(
            ["sudo", "pfctl", "-t", "blocked", "-T", "add", ip_address], check=False
        )


if __name__ == "__main__":
    monitor = SecurityMonitor()

    # Starte Live-Überwachung
    monitor.detect_intrusions()
    print("🔍 Überwachung gestartet...")