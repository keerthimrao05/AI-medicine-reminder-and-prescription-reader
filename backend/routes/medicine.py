from flask import Blueprint

medicine_bp = Blueprint("medicine", __name__)

@medicine_bp.route("/medicines", methods=["GET"])
def medicines():

    return {
        "status": True,
        "message": "Medicine Route Working"
    }