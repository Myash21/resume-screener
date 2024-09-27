// App.jsx
import React from "react";
import ResumeUploader from "./ResumeUploader";
import LLMQueryComponent from "./LLMQueryComponent";
import './index.css';

function App() {
  return (
    <div className="App relative" style={{ overflow: 'hidden', backgroundColor: '#001f3f', minHeight: '100vh' }}>
      <ResumeUploader />
      <LLMQueryComponent />
    </div>
  );
}

export default App;
