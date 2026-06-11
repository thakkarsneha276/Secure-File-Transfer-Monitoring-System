from flask import Flask, jsonify, render_template
import json
import os

app = Flask(__name__, template_folder="templates")

LOG_FILE = "../data/logs.json"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/logs")
def logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return jsonify(json.load(f))
    return jsonify([])


@app.route("/summary")
def summary():

    if os.path.exists(LOG_FILE):

        with open(LOG_FILE, "r") as f:
            data = json.load(f)

        created = sum(1 for x in data if x["event"] == "CREATED")
        modified = sum(1 for x in data if x["event"] == "MODIFIED")
        moved = sum(1 for x in data if x["event"] == "MOVED")
        deleted = sum(1 for x in data if x["event"] == "DELETED")

        return jsonify({
            "total": len(data),
            "created": created,
            "modified": modified,
            "moved": moved,
            "deleted": deleted
        })

    return jsonify({
        "total": 0,
        "created": 0,
        "modified": 0,
        "moved": 0,
        "deleted": 0
    })

@app.route("/alerts")
def alerts():

    if os.path.exists(LOG_FILE):

        with open(LOG_FILE, "r") as f:
            data = json.load(f)

        alerts = []

        for entry in data:

            extra = entry.get("extra", {})
            analysis = extra.get("analysis", {})

            if analysis.get("sensitive"):
                alerts.append({
                    "time": entry["time"],
                    "event": entry["event"],
                    "file": entry["file"]
                })

        return jsonify(alerts)

    return jsonify([])

if __name__ == "__main__":
    app.run(debug=True)