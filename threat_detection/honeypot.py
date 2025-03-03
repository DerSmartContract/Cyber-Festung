import time
import random


class Honeypot:
    def __init__(self):
        self.attempts = []

    def detect_intruder(self, ip):
        print(f"⚠️ Intrusion detected from {ip}! Logging attempt...")
        self.attempts.append({"ip": ip, "timestamp": time.time()})

    def generate_fake_system(self):
        print("Simulating vulnerable system...")
        time.sleep(2)
        print("Fake ports open: 22, 80, 443")
        return True


if __name__ == "__main__":
    hp = Honeypot()
    hp.generate_fake_system()
    hp.detect_intruder(f"192.168.1.{random.randint(2, 254)}")
