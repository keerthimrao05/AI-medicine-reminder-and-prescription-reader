from rapidfuzz import process
from services.medicine_db import MEDICINES

def extract_medicines(ocr_text):

    found = []

    for line in ocr_text:

        line = line.strip()

        if len(line) < 3:
            continue

        match = process.extractOne(line, MEDICINES)

        if match and match[1] > 70:

            medicine = match[0]

            if medicine not in found:
                found.append(medicine)

    return found