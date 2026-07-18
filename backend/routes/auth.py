from flask import Blueprint, request, jsonify
from models.User import users
import bcrypt
import jwt
import datetime
from config import Config

auth_bp = Blueprint("auth", __name__)


# ---------------- REGISTER ---------------- #

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")
    age = data.get("age")

    if not all([name, email, password]):
        return jsonify({
            "status": False,
            "message": "All required fields must be filled"
        }), 400

    existing = users.find_one({"email": email})

    if existing:
        return jsonify({
            "status": False,
            "message": "Email already registered"
        }), 400

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    users.insert_one({

        "name": name,
        "email": email,
        "password": hashed_password,
        "phone": phone,
        "age": age,
        "created_at": datetime.datetime.utcnow()

    })

    return jsonify({

        "status": True,
        "message": "Registration Successful"

    })


# ---------------- LOGIN ---------------- #

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = users.find_one({"email": email})

    if user is None:

        return jsonify({

            "status": False,
            "message": "User not found"

        }), 404

    if not bcrypt.checkpw(
        password.encode("utf-8"),
        user["password"]
    ):

        return jsonify({

            "status": False,
            "message": "Invalid Password"

        }), 401

    token = jwt.encode(

        {
            "email": user["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
        },

        Config.JWT_SECRET,
        algorithm="HS256"

    )

    return jsonify({

        "status": True,
        "message": "Login Successful",
        "token": token,
        "name": user["name"]

    })