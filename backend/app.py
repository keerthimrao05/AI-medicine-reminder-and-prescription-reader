from flask import Flask
from flask_cors import CORS

from routes.auth import auth_bp
from routes.prescription import prescription_bp
from routes.medicine import medicine_bp
from routes.reminder import reminder_bp
from routes.dashboard import dashboard_bp

app = Flask(__name__)

CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(prescription_bp)
app.register_blueprint(medicine_bp)
app.register_blueprint(reminder_bp)
app.register_blueprint(dashboard_bp)

@app.route("/")
def home():

    return {
        "status": True,
        "message": "AI Medicine Reminder Backend Running"
    }

if __name__ == "__main__":

    app.run(debug=True, use_reloader=False)