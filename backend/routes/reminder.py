from flask import Blueprint, request, jsonify
from models.Reminder import reminders

reminder_bp = Blueprint("reminder", __name__)


@reminder_bp.route("/reminders", methods=["POST"])
def add_reminder():

    data = request.json

    reminder = {
        "medicine": data["medicine"],
        "time": data["time"],
        "days": data["days"]
    }

    reminders.insert_one(reminder)

    return jsonify({
        "status": True,
        "message": "Reminder Added Successfully"
    })


@reminder_bp.route("/reminders", methods=["GET"])
def get_reminders():

    data = list(reminders.find({}, {"_id": 0}))

    return jsonify({
        "status": True,
        "reminders": data
    })