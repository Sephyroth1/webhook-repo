import os

from dotenv import dotenv_values
from flask import Flask, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)
config = dotenv_values(".env")

app.mongodb_client = MongoClient(config["MONGO_URL"])
app.database = app.mongodb_client[config["DATABASE"]]
app.collection = app.database["github_events"]


@app.route("/")
def hello_world():
    return "Webhook Server Running!"


@app.route("/webhook", methods=["POST"])
def webhook():
    print("Webhook hit!")
    print("Headers:", request.headers)
    payload = request.json
    print("Payload:", payload)

    event = request.headers.get("X-GitHub-Event")
    print("Event type:", event)

    data = None
    if event == "push":
        data = {
            "action": "PUSH",
            "author": payload["pusher"]["name"],
            "from_branch": None,
            "to_branch": payload["ref"].split("/")[-1],
            "timestamp": payload["head_commit"]["timestamp"],
            "request_id": payload["head_commit"]["id"],
        }

    elif event == "pull_request":
        # MERGE case
        if payload["action"] == "closed" and payload["pull_request"]["merged"]:
            data = {
                "action": "MERGE",
                "author": payload["pull_request"]["merged_by"]["login"],
                "from_branch": payload["pull_request"]["head"]["ref"],
                "to_branch": payload["pull_request"]["base"]["ref"],
                "timestamp": payload["pull_request"]["merged_at"],
                "request_id": payload["pull_request"]["id"],
            }
        else:
            # Normal PR
            data = {
                "action": "PULL_REQUEST",
                "author": payload["pull_request"]["user"]["login"],
                "from_branch": payload["pull_request"]["head"]["ref"],
                "to_branch": payload["pull_request"]["base"]["ref"],
                "timestamp": payload["pull_request"]["created_at"],
                "request_id": payload["pull_request"]["id"],
            }

    if data:
        app.collection.insert_one(data)
        return {"status": "stored"}, 200
    else:
        return {"status": "ignored"}, 200


@app.route("/events", methods=["GET"])
def get_events():
    # Get latest 10 events, newest first
    events = list(app.collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(10))
    return events, 200
