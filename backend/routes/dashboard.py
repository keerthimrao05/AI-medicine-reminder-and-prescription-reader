from flask import Blueprint

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard", methods=["GET"])
def dashboard():

    return {
        "status": True,
        "message": "Dashboard Route Working"
    }