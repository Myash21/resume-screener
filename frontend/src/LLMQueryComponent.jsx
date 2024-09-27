import React, { useState } from "react";
import axios from "axios";

const LLMQueryComponent = () => {
  const [jobDescription, setJobDescription] = useState("");
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await axios.post("http://127.0.0.1:5000/api/predict", {
        job_description: jobDescription,
        question: question,
      });

      if (res.data.answer) {
        setResponse(res.data.answer);
        setError("");
      } else {
        setError("No response from the server.");
      }
    } catch (err) {
      console.error(err);
      setError("An error occurred while processing your request.");
    }
  };

  return (
    <div className="container">
      <h2>Ask LLM about Candidates</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="jobDescription">Job Description:</label>
          <textarea
            id="jobDescription"
            className="form-control"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Enter job description"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="question">Question:</label>
          <input
            id="question"
            type="text"
            className="form-control"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Enter your question"
            required
          />
        </div>

        <button type="submit" className="btn btn-primary mt-3">
          Submit
        </button>
      </form>

      {response && (
        <div className="response mt-4">
          <h4>Response:</h4>
          <p>{response}</p>
        </div>
      )}

      {error && (
        <div className="error mt-4">
          <p style={{ color: "red" }}>{error}</p>
        </div>
      )}
    </div>
  );
};

export default LLMQueryComponent;
