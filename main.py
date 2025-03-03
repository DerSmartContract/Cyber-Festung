from security_core.auth_manager import AuthManager
from security_core.access_control import AccessControl
from threat_detection.honeypot import Honeypot
from stealth_ops.fake_logs import FakeLogs


def main():
    auth = AuthManager()
    access = AccessControl()
    honeypot = Honeypot()
    logs = FakeLogs()

    print("\n🔒 Fortress Security System gestartet...\n")

    print(auth.register("testuser", "password123"))
    print(auth.login("testuser", "password123"))

    print(access.check_access("testuser", "write"))

    honeypot.generate_fake_system()
    honeypot.detect_intruder("192.168.1.99")

    logs.print_logs()


if __name__ == "__main__":
    main()
