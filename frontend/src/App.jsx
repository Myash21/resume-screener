import React from "react";
import ResumeUploader from "./ResumeUploader";
import LLMQueryComponent from "./LLMQueryComponent";
import './index.css';

function App() {
  return (
    <div className="App">
      <ResumeUploader />
      <LLMQueryComponent />
    </div>
  );
}

export default App;
