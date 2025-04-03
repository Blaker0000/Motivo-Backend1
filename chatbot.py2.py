import os
import openai
import json
import sqlite3
import smartsheet
from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# SmartSheet API client
smart = smartsheet.Smartsheet(os.getenv("SMARTSHEET_API_KEY"))

# Memory database setup
MEMORY_DB = "chatbot_memory.db"
if not os.path.exists(MEMORY_DB):
    conn = sqlite3.connect(MEMORY_DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT
        )
    """)
    conn.commit()
    conn.close()

# Save Q&A to memory
def save_to_memory(question, answer):
    conn = sqlite3.connect(MEMORY_DB)
    c = conn.cursor()
    c.execute("INSERT INTO memory (question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()
    conn.close()

# OpenAI Chat Endpoint
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")

    messages = [
        {"role": "system", "content": "You are a helpful assistant for Motivo Group operations."},
        {"role": "user", "content": question}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        answer = response.choices[0].message.content.strip()
        save_to_memory(question, answer)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# PDF Summarization
@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    file = request.files["pdf"]
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    prompt = f"Summarize the following document:
{text[:3000]}"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        summary = response.choices[0].message.content.strip()
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add row to SmartSheet
@app.route("/smartsheet/<sheet_id>/add_row", methods=["POST"])
def add_row(sheet_id):
    data = request.json
    new_row = smartsheet.models.Row()
    new_row.to_top = True
    new_row.cells = [
        smartsheet.models.Cell(column_id=int(col_id), value=value)
        for col_id, value in data.items()
    ]
    response = smart.Sheets.add_rows(sheet_id, [new_row])
    return jsonify({"result": "Row added", "response": response.message})

# SmartSheet summary placeholder
@app.route("/smartsheet/<sheet_id>/summary", methods=["GET"])
def summary(sheet_id):
    try:
        sheet = smart.Sheets.get_sheet(sheet_id).to_dict()
        return jsonify({"summary": {
            "sheet_name": sheet["name"],
            "total_rows": len(sheet["rows"]),
            "columns": [col["title"] for col in sheet["columns"]]
        }})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Launch the chatbot server
if __name__ == "__main__":
    app.run(port=5001, debug=True)
