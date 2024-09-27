from flask import Flask, render_template, jsonify, request
import logging
from flask_cors import CORS

from utils import query_rag

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static",
)

logging.basicConfig(level=logging.INFO)


CORS(
    app,
    resources={
        r"/*": {"origins": ["*", "http://localhost:5173", "http://127.0.0.1:5000"]}
    },
)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/job_description")
def get_job_desription():
    job_desription = request.form.get("job_description") 
    print(job_desription)
    return job_desription

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
