// LLMQueryComponent.jsx
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
        setResponse(formatResponse(res.data.answer));
        setError("");
      } else {
        setError("No response from the server.");
      }
    } catch (err) {
      console.error(err);
      setError("An error occurred while processing your request.");
    }
  };

  const formatResponse = (text) => {
    text = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    text = text.replace(/\*\*\*(.*?)\*\*\*/g, "<em><strong>$1</strong></em>");
    text = text.replace(/\*(.*?)\*/g, "<em>$1</em>");
    text = text.replace(/\n/g, "<br />");
    return text;
  };

  return (
    <div className=" w-full lg:w-3/5  mx-auto p-6 bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold text-center mb-6 text-blue-700">
        Ask LLM about Candidates
      </h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label
            htmlFor="question"
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            Question:
          </label>
          <input
            id="question"
            type="text"
            className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Enter your question"
            required
          />
        </div>
        <button
          type="submit"
          className="w-full py-2 px-4 bg-blue-600 text-white font-semibold rounded-md hover:bg-blue-700 transition-colors"
        >
          Submit
        </button>
      </form>
      {response && (
        <div
          className="mt-6 p-4 bg-green-100 border border-green-400 text-green-700 rounded overflow-y-auto"
          style={{ maxHeight: "350px" }}
        >
          <h4 className="font-semibold">Response:</h4>
          <p dangerouslySetInnerHTML={{ __html: response }} />
        </div>
      )}
      {error && (
        <div className="mt-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          <p>{error}</p>
        </div>
      )}
    </div>
  );
};

export default LLMQueryComponent;
