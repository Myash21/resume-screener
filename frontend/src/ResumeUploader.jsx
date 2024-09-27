import React, { useState } from 'react';
import axios from 'axios';

const ResumeUploader = () => {
    const [selectedFiles, setSelectedFiles] = useState([]);
    const [jobDescription, setJobDescription] = useState('');
    const [responseMessage, setResponseMessage] = useState('');

    // Handle folder selection (get multiple files)
    const handleFolderChange = (e) => {
        const files = Array.from(e.target.files);
        setSelectedFiles(files.filter(file => file.type === "application/pdf"));  // Only PDFs
    };

    const handleJobDescriptionChange = (e) => {
        setJobDescription(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (selectedFiles.length === 0 || !jobDescription) {
            alert("Please select a folder with PDF files and provide a job description.");
            return;
        }

        // Create FormData for each file
        const formData = new FormData();
        selectedFiles.forEach((file) => {
            formData.append("resumes", file);
        });
        formData.append("job_description", jobDescription);

        try {
            const response = await axios.post('http://127.0.0.1:5000/api/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            setResponseMessage(response.data.message);
        } catch (error) {
            console.error("Error uploading resumes and job description", error);
            setResponseMessage("Failed to upload resumes.");
        }
    };

    const handleReset = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:5000/api/reset');
            setResponseMessage(response.data.message);
        } catch (error) {
            console.error("Error resetting uploads", error);
            setResponseMessage("Failed to reset uploads.");
        }
    };

    return (
        <div>
            <h1>Upload Resumes and Job Description</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Select Folder (PDFs only):</label>
                    <input 
                        type="file"
                        webkitdirectory="true"  // Select entire folder
                        directory="true"
                        onChange={handleFolderChange}
                        multiple
                    />
                </div>
                <div>
                    <label>Job Description:</label>
                    <textarea
                        value={jobDescription}
                        onChange={handleJobDescriptionChange}
                        placeholder="Enter the job description here"
                        rows="4"
                        cols="50"
                    />
                </div>
                <button type="submit">Submit</button>
                <button type="button" onClick={handleReset}>Reset Uploads</button>
            </form>
            {responseMessage && <p>{responseMessage}</p>}
        </div>
    );
};

export default ResumeUploader;
