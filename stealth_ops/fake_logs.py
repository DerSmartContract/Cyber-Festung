import random


class FakeLogs:
    def __init__(self):
        self.logs = []

    def generate_log(self, event_type="INFO"):
        fake_log = f"{event_type}: System running normally. No threats detected."
        if random.random() > 0.8:
            fake_log = f"{event_type}: Potential anomaly detected. Investigating..."
        self.logs.append(fake_log)
        return fake_log

    def print_logs(self):
        for log in self.logs:
            print(log)


if __name__ == "__main__":
    fl = FakeLogs()
    for _ in range(5):
        print(fl.generate_log())
