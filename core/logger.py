import json
import os
from datetime import datetime


class Logger:

    def __init__(self, file="data/logs.json"):
        self.file = file
        os.makedirs("data", exist_ok=True)

    def log(self, event, path, extra=None):

        data = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "event": event,
            "file": path,
            "extra": extra or {}
        }

        logs = []

        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                try:
                    logs = json.load(f)
                except:
                    logs = []

        logs.append(data)

        with open(self.file, "w") as f:
            json.dump(logs, f, indent=4)

        print(f"[LOG] {event} -> {path}")