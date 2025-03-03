import random
from utils.logger import Logger


class FakeLogs:
    def __init__(self):
        self.logger = Logger()

    def generate_log(self, event_type="INFO"):
        fake_log = f"{event_type}: System running normally. No threats detected."
        if random.random() > 0.8:
            fake_log = f"{event_type}: Potential anomaly detected. Investigating..."

        self.logger.log_event(event_type, fake_log)  # In SQLite speichern
        return fake_log

    def print_logs(self):
        logs = self.logger.get_logs(5)
        for log in logs:
            print(log)


if __name__ == "__main__":
    fl = FakeLogs()
    for _ in range(5):
        print(fl.generate_log())
