from flask import Flask, request, send_file, redirect
import os
import pandas as pd
from datetime import datetime

app = Flask(__name__)

EXCEL_FILE = "feedback_responses.xlsx"

@app.route("/")
def index():
    return open("feedback-form/index.html").read()

@app.route("/submit", methods=["POST"])
def submit():
    data = request.form.to_dict(flat=False)  # Grab checkboxes as lists
    flat_data = {k: (", ".join(v) if isinstance(v, list) else v) for k, v in data.items()}
    flat_data["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Load or create DataFrame
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
    else:
        df = pd.DataFrame()

    # Append new row
    df = pd.concat([df, pd.DataFrame([flat_data])], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)

    return redirect("/")  # Or show a thank-you page

@app.route("/download")
def download():
    return send_file(EXCEL_FILE, as_attachment=True)
    
@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('feedback-form/css', path)

@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('feedback-form/assets', path)


