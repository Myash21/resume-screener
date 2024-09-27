import os
import logging
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from utils import query_rag

# Flask configuration
app = Flask(
    __name__,
    template_folder="../frontend/templates",  # Existing template path
    static_folder="../frontend/static"        # Existing static path
)

logging.basicConfig(level=logging.INFO)

CORS(
    app,
    resources={
        r"/*": {"origins": ["*", "http://localhost:5173", "http://127.0.0.1:5000"]}
    },
)

# Folder for uploading resumes
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Existing route to render the index page
@app.get("/")
def index():
    return render_template("index.html")

# Route to get job description from frontend
@app.post("/job_description")
def get_job_desription():
    job_description = request.form.get("job_description") 
    print(job_description)
    return job_description

# Route for resume upload and job description submission
@app.post("/api/upload")
def upload_resumes():
    if 'resumes' not in request.files or 'job_description' not in request.form:
        return jsonify({"error": "Resumes and job description are required."}), 400
    
    job_description = request.form['job_description']
    uploaded_files = request.files.getlist('resumes')  # Get the list of files

    if not uploaded_files:
        return jsonify({"error": "No files were uploaded."}), 400

    saved_files = []
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            saved_files.append(filename)

    return jsonify({
        "message": "Resumes and job description received successfully.",
        "saved_files": saved_files,
        "job_description": job_description
    }), 200

# Prediction route (unchanged)
@app.post("/predict")
def predict():
    try:
        data = request.json
        if not data or "message" not in data:
            logging.error("Invalid input: No message field in request data.")
            return jsonify({"answer": "No message provided"})

        message = data["message"]
        response, response_links = query_rag(query_text=message)
        return jsonify({"answer": response, "links": response_links})

    except Exception as e:
        logging.error(f"Error in /predict: {e}")
        return jsonify({"answer": "An error occurred while processing your request."})


if __name__ == "__main__":
    app.run(debug=True)
