import os
import logging
from utils import query_rag
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Flask configuration
app = Flask(
    __name__,
    template_folder="../frontend/templates",  # Existing template path
    static_folder="../frontend/static",  # Existing static path
)

logging.basicConfig(level=logging.INFO)

CORS(
    app,
    resources={
        r"/*": {"origins": ["*", "http://localhost:5173", "http://127.0.0.1:5000"]}
    },
)

# Folder for uploading resumes
UPLOAD_FOLDER = "./uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the upload folders exist
jd_path = os.path.join(UPLOAD_FOLDER, "jd")
pdfs_path = os.path.join(UPLOAD_FOLDER, "pdfs")
os.makedirs(jd_path, exist_ok=True)
os.makedirs(pdfs_path, exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Existing route to render the index page
@app.get("/")
def index():
    return render_template("index.html")


# Route for resume upload and job description submission
@app.post("/api/upload")
def upload_resumes():
    if "resumes" not in request.files or "job_description" not in request.form:
        return jsonify({"error": "Resumes and job description are required."}), 400

    job_description = request.form["job_description"]
    uploaded_files = request.files.getlist("resumes")  # Get the list of files

    if not uploaded_files:
        return jsonify({"error": "No files were uploaded."}), 400

    saved_files = []
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(pdfs_path, filename))  # Save PDFs in /uploads/pdfs
            saved_files.append(filename)

    # Save job description as text file
    with open(os.path.join(jd_path, "job_description.txt"), "w") as jd_file:
        jd_file.write(job_description)

    return jsonify(
        {
            "message": "Resumes and job description received successfully.",
            "saved_files": saved_files,
            "job_description": job_description,
        }
    ), 200


# Route for resetting uploads
@app.post("/api/reset")
def reset_uploads():
    try:
        # Remove all files in the job description and PDF folders
        for folder in [jd_path, pdfs_path]:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)

        return jsonify({"message": "Uploads reset successfully."}), 200

    except Exception as e:
        logging.error(f"Error resetting uploads: {e}")
        return jsonify({"error": "Failed to reset uploads."}), 500


# Prediction route (unchanged)
@app.post("/predict")
def predict():
    try:
        data = request.json
        if not data or "message" not in data:
            logging.error("Invalid input: No message field in request data.")
            return jsonify({"answer": "No message provided"})

        message = data["message"]
        response, response_links = query_rag(job_description=message)
        return jsonify({"answer": response, "links": response_links})

    except Exception as e:
        logging.error(f"Error in /predict: {e}")
        return jsonify({"answer": "An error occurred while processing your request."})


if __name__ == "__main__":
    app.run(debug=True)
