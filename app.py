from flask import Flask, request, send_file, redirect, render_template
import os
import pandas as pd
from datetime import datetime

app = Flask(__name__)

EXCEL_FILE = "feedback_responses.xlsx"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.form.to_dict(flat=False)  # Grab checkboxes as lists
    flat_data = {k: ", ".join(v) if isinstance(v, list) else v for k, v in data.items()}
    flat_data["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Load or create DataFrame
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
    else:
        df = pd.DataFrame()

    df = pd.concat([df, pd.DataFrame([flat_data])], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)

    return redirect("/thank-you")

@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html")

@app.route("/download")
def download():
    if os.path.exists(EXCEL_FILE):
        return send_file(EXCEL_FILE, as_attachment=True)
    else:
        return "No feedback collected yet.", 404

