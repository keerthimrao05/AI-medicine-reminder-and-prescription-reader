from flask import Blueprint, request, jsonify
import os
import cv2
import easyocr

from services.medicine_parser import extract_medicines
from models.Medicine import medicines

prescription_bp = Blueprint("prescription", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load EasyOCR once
reader = easyocr.Reader(["en"])


@prescription_bp.route("/uploadPrescription", methods=["POST"])
def upload():

    # Check file
    if "file" not in request.files:
        return jsonify({
            "status": False,
            "message": "No file uploaded"
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "status": False,
            "message": "No file selected"
        }), 400

    # Save image
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Read image
    img = cv2.imread(filepath)

    if img is None:
        return jsonify({
            "status": False,
            "message": "Invalid image"
        }), 400

    # Preprocess image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    _, thresh = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # Save processed image
    cv2.imwrite(filepath, thresh)

    # OCR
    ocr_text = reader.readtext(filepath, detail=0)

    # Extract medicine names
    medicine_list = extract_medicines(ocr_text)

    # Save medicines to MongoDB
    for med in medicine_list:

        # Avoid duplicates
        if medicines.find_one({"medicine": med}) is None:

            medicines.insert_one({
                "medicine": med
            })

    return jsonify({

        "status": True,
        "message": "Prescription Uploaded Successfully",
        "filename": file.filename,
        "ocr_text": ocr_text,
        "medicines": medicine_list

    })