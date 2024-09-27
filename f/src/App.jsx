import React from "react";
import ResumeUploader from "./ResumeUploader";
import ChatApp from "./ChatApp";
import LLMQueryComponent from "./LLMQueryComponent";
import './index.css';

function App() {
  return (
    <div className="App">
      <ResumeUploader />
      <ChatApp />
      <LLMQueryComponent />
    </div>
  );
}

export default App;
