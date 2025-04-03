import os
import json
import logging
import fitz  ￼# PyMuPDF
import openai
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

# === CONFIGURATION ===
SOP_FOLDER = "C:/Users/blake/Desktop/MotivoSystem/motivo_backend/dashboard_data/sops"
PDF_FOLDER = os.path.join(SOP_FOLDER, "pdfs")
AUTOMATION_SCRIPTS = "C:/Users/blake/Desktop/MotivoSystem/motivo_backend/automation_scripts"
os.makedirs(SOP_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(AUTOMATION_SCRIPTS, exist_ok=True)
logging.basicConfig(level=logging.INFO)

# === LOAD SOP DATA ===
def load_sop_data():
    sops = []
    for filename in os.listdir(SOP_FOLDER):
        if filename.endswith(".json"):
            try:
                with open(os.path.join(SOP_FOLDER, filename), "r") as f:
                    sops.append(json.load(f))
            except Exception as e:
                logging.warning(f"Failed to load {filename}: {e}")
    return sops

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# === ROUTES ===

@app.route("/api/sops", methods=["GET"])
def get_sops():
    try:
        data = load_sop_data()
        return jsonify({"status": "success", "sops": data})
    except Exception as e:
        logging.error(f"Error loading SOPs: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/sops/pdf/<filename>", methods=["GET"])
def get_sop_pdf(filename):
    try:
        return send_from_directory(PDF_FOLDER, filename)
    except Exception as e:
        logging.error(f"Error serving PDF {filename}: {e}")
        return jsonify({"status": "error", "message": str(e)}), 404

@app.route("/api/sops/upload_pdf", methods=["POST"])
def upload_pdf():
    try:
        if 'file' not in request.files or 'sop_id' not in request.form:
            return jsonify({"status": "error", "message": "Missing file or SOP ID"}), 400
        file = request.files['file']
        sop_id = request.form['sop_id'].replace(" ", "_")
        if file.filename == '':
            return jsonify({"status": "error", "message": "No file selected"}), 400
        filename = secure_filename(f"{sop_id}.pdf")
        file_path = os.path.join(PDF_FOLDER, filename)
        file.save(file_path)
        logging.info(f"PDF uploaded for SOP {sop_id}: {filename}")
        return jsonify({"status": "success", "message": f"PDF uploaded for SOP {sop_id}", "file_path": file_path})
    except Exception as e:
        logging.error(f"Error uploading PDF: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/sops/summarize_pdf/<sop_id>", methods=["POST"])
def summarize_pdf(sop_id):
    try:
        pdf_path = os.path.join(PDF_FOLDER, f"{sop_id}.pdf")
        if not os.path.exists(pdf_path):
            return jsonify({"status": "error", "message": "PDF not found for summarization"}), 404
        document_text = extract_text_from_pdf(pdf_path)
        if len(document_text.strip()) == 0:
            return jsonify({"status": "error", "message": "PDF is empty or unreadable"}), 400
        api_key = os.getenv("OPENAI_API_KEY", "sk-REPLACE_ME")
        if "sk-" not in api_key:
            return jsonify({"status": "error", "message": "OpenAI API key not configured."}), 403
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in oil refinery operations and SOP documentation."},
                {"role": "user", "content": f"Summarize the following SOP document:\n\n{document_text[:7000]}"}
            ],
            temperature=0.3,
            max_tokens=600
        )
        summary_text = response.choices[0].message.content.strip()
        json_path = os.path.join(SOP_FOLDER, f"dashboard_sop_{sop_id}.json")
        if not os.path.exists(json_path):
            return jsonify({"status": "error", "message": "Associated SOP JSON not found"}), 404
        with open(json_path, "r") as f:
            sop_data = json.load(f)
        sop_data["summary"] = summary_text
        with open(json_path, "w") as f:
            json.dump(sop_data, f, indent=4)
        return jsonify({
            "status": "success",
            "message": "Summary generated and saved.",
            "summary": summary_text
        })
    except Exception as e:
        logging.error(f"GPT summarization failed: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# === MAIN ===
if __name__ == "__main__":
    app.run(debug=True, port=5000)