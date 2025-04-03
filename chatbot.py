import os
import json
import logging
import fitz  # PyMuPDF
import openai
import smtplib
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from email.mime.text import MIMEText
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# === CONFIGURATION ===
SOP_FOLDER = "C:/Users/blake/Desktop/MotivoSystem/motivo_backend/dashboard_data/sops"
PDF_FOLDER = os.path.join(SOP_FOLDER, "pdfs")
AUTOMATION_SCRIPTS = os.path.join(SOP_FOLDER, "scripts")
os.makedirs(SOP_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(AUTOMATION_SCRIPTS, exist_ok=True)
logging.basicConfig(level=logging.INFO)

# === HELPERS ===
def load_sops():
    sops = []
    for f in os.listdir(SOP_FOLDER):
        if f.endswith(".json"):
            with open(os.path.join(SOP_FOLDER, f), "r") as file:
                sops.append(json.load(file))
    return sops

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    return "".join([page.get_text() for page in doc])

# === ROUTES ===
@app.route("/api/status", methods=["GET"])
def api_status():
    status = {
        "flask": "🟢",
        "gpt": "🟢" if "sk-" in os.getenv("OPENAI_API_KEY", "") else "🔴",
        "smartsheet": "🟢" if "sk-" in os.getenv("SMARTSHEET_API_TOKEN", "") else "🔴",
        "sharepoint": "🟢" if "sharepoint.com" in os.getenv("SHAREPOINT_URL", "") else "🔴"
    }
    return jsonify({"status": "ok", "services": status})

@app.route("/api/sops", methods=["GET"])
def get_sops():
    return jsonify({"status": "success", "sops": load_sops()})

@app.route("/api/sops/upload_pdf", methods=["POST"])
def upload_pdf():
    if 'file' not in request.files or 'sop_id' not in request.form:
        return jsonify({"status": "error", "message": "Missing file or SOP ID"}), 400
    file = request.files['file']
    sop_id = request.form['sop_id'].replace(" ", "_")
    filename = secure_filename(f"{sop_id}.pdf")
    file_path = os.path.join(PDF_FOLDER, filename)
    file.save(file_path)
    return jsonify({"status": "success", "message": f"Uploaded {filename}."})

@app.route("/api/sops/summarize_pdf/<sop_id>", methods=["POST"])
def summarize_pdf(sop_id):
    pdf_path = os.path.join(PDF_FOLDER, f"{sop_id}.pdf")
    if not os.path.exists(pdf_path):
        return jsonify({"status": "error", "message": "PDF not found"}), 404
    document_text = extract_text_from_pdf(pdf_path)
    openai.api_key = os.getenv("OPENAI_API_KEY", "")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in SOP and safety documentation."},
            {"role": "user", "content": f"Summarize this SOP:\n\n{document_text[:7000]}"}
        ],
        temperature=0.3,
        max_tokens=600
    )
    summary = response.choices[0].message.content.strip()
    sop_file = os.path.join(SOP_FOLDER, f"dashboard_sop_{sop_id}.json")
    if os.path.exists(sop_file):
        with open(sop_file, "r") as f:
            sop_data = json.load(f)
        sop_data["summary"] = summary
        with open(sop_file, "w") as f:
            json.dump(sop_data, f, indent=4)
    return jsonify({"status": "success", "summary": summary})

@app.route("/api/sops/chat_command", methods=["POST"])
def chat_command():
    command = request.json.get("command", "")
    if not command.lower().startswith("!add_sop"):
        return jsonify({"status": "error", "message": "Invalid command"}), 400
    parts = command.strip().split(" ", 2)
    sop_id, title = parts[1], parts[2]
    sop_data = {
        "document_number": sop_id,
        "title": title,
        "prepared_by": "Blake DeRango",
        "effective_date": "2025-03-31",
        "link_to_pdf": f"https://sharepoint.com/docs/{sop_id}.pdf",
        "status": "Active",
        "summary": ""
    }
    with open(os.path.join(SOP_FOLDER, f"dashboard_sop_{sop_id}.json"), "w") as f:
        json.dump(sop_data, f, indent=4)
    return jsonify({"status": "success", "message": f"SOP {sop_id} created."})

@app.route("/api/email_report", methods=["POST"])
def email_report():
    try:
        sops = load_sops()
        missing_summary = [s["document_number"] for s in sops if not s.get("summary")]
        body = f"""SOP REPORT:
Missing Summaries: {len(missing_summary)}
{', '.join(missing_summary)}
        """
        msg = MIMEText(body)
        msg["Subject"] = "Daily SOP Report"
        msg["From"] = os.getenv("EMAIL_FROM")
        msg["To"] = os.getenv("EMAIL_TO")

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(os.getenv("EMAIL_FROM"), os.getenv("EMAIL_PASS"))
            server.sendmail(msg["From"], msg["To"], msg.as_string())

        return jsonify({"status": "success", "message": "Email sent"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/api/sops/sync_sharepoint/<sop_id>", methods=["POST"])
def sync_sharepoint(sop_id):
    return jsonify({"status": "todo", "message": "SharePoint sync stub - add Graph API here."})

if __name__ == "__main__":
    app.run(debug=True, port=5000)