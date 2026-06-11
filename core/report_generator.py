import json
import os


class ReportGenerator:

    def generate(self):

        log_file = "data/logs.json"
        report_file = "data/final_report.txt"

        if not os.path.exists(log_file):
            print("No logs found.")
            return

        with open(log_file, "r") as f:
            logs = json.load(f)

        created = sum(1 for x in logs if x["event"] == "CREATED")
        modified = sum(1 for x in logs if x["event"] == "MODIFIED")
        moved = sum(1 for x in logs if x["event"] == "MOVED")
        deleted = sum(1 for x in logs if x["event"] == "DELETED")

        alerts = []

        for entry in logs:
            analysis = entry.get("extra", {}).get("analysis", {})

            if analysis.get("sensitive"):
                alerts.append(entry)

        report = []

        report.append("=" * 40)
        report.append("SECURE FILE MONITOR AUDIT REPORT")
        report.append("=" * 40)

        report.append("")
        report.append(f"Total Events: {len(logs)}")
        report.append(f"Created: {created}")
        report.append(f"Modified: {modified}")
        report.append(f"Moved: {moved}")
        report.append(f"Deleted: {deleted}")

        report.append("")
        report.append(f"Sensitive Alerts: {len(alerts)}")

        report.append("")
        report.append("Alert Details:")
        report.append("-" * 40)

        for alert in alerts:

            report.append(alert["time"])
            report.append(alert["event"])
            report.append(alert["file"])
            report.append("")

        with open(report_file, "w") as f:
            f.write("\n".join(report))

        print(f"Report generated -> {report_file}")