// App.jsx
import React from 'react';
import LLMQueryComponent from './LLMQueryComponent';
import ResumeUploader from './ResumeUploader';

const App = () => {
  return (
    <div className="container mx-auto p-4" style={{ overflow: 'hidden', backgroundColor: '#001f3f', minHeight: '100vh' }}>
      {/* Responsive layout: 2 columns on large screens, 1 column on small screens */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
     
        <ResumeUploader />
        <LLMQueryComponent />
      </div>
    </div>
  );
};

export default App;
