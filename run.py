import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from core.hash_util import HashUtil
from core.logger import Logger
from core.rule_engine import RuleEngine


class MonitorHandler(FileSystemEventHandler):

    def __init__(self):
        self.hash_util = HashUtil()
        self.logger = Logger()
        self.rules = RuleEngine()

    # ---------------- CREATED ----------------
    def on_created(self, event):
        if not event.is_directory:

            analysis = self.rules.analyze(event.src_path)

            time.sleep(0.2)

            file_hash = self.hash_util.generate_hash(event.src_path)

            if analysis["sensitive"]:
                print("⚠ ALERT: Sensitive file created!")

            self.logger.log(
                "CREATED",
                event.src_path,
                {
                    "hash": file_hash,
                    "analysis": analysis
                }
            )

            print(f"[CREATED] {event.src_path}")

    # ---------------- MODIFIED ----------------
    def on_modified(self, event):
        if not event.is_directory:

            analysis = self.rules.analyze(event.src_path)

            file_hash = self.hash_util.generate_hash(event.src_path)

            if analysis["sensitive"]:
                print("⚠ ALERT: Sensitive file modified!")

            self.logger.log(
                "MODIFIED",
                event.src_path,
                {
                    "hash": file_hash,
                    "analysis": analysis
                }
            )

            print(f"[MODIFIED] {event.src_path}")

    # ---------------- DELETED ----------------
    def on_deleted(self, event):
        if not event.is_directory:

            self.logger.log(
                "DELETED",
                event.src_path,
                {}
            )

            print(f"[DELETED] {event.src_path}")

    # ---------------- MOVED ----------------
    def on_moved(self, event):
        if not event.is_directory:

            analysis = self.rules.analyze(event.dest_path)

            if analysis["sensitive"] or analysis["external"]:
                print("⚠ ALERT: Suspicious file movement detected!")

            self.logger.log(
                "MOVED",
                event.src_path,
                {
                    "destination": event.dest_path,
                    "analysis": analysis
                }
            )

            print(f"[MOVED FROM] {event.src_path}")
            print(f"[MOVED TO]   {event.dest_path}")


if __name__ == "__main__":

    watch_folder = "workspace"

    observer = Observer()
    observer.schedule(MonitorHandler(), path=watch_folder, recursive=True)
    observer.start()

    print("\n🔐 Secure File Monitor Running...")
    print(f"📁 Watching folder: {watch_folder}\n")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping monitor...")
        observer.stop()

    observer.join()