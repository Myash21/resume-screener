import React, { useState } from 'react';
import axios from 'axios';

const ResumeUploader = () => {
    const [selectedFiles, setSelectedFiles] = useState([]);
    const [jobDescription, setJobDescription] = useState('');
    const [responseMessage, setResponseMessage] = useState('');

    const handleFolderChange = (e) => {
        const files = Array.from(e.target.files);
        setSelectedFiles(files.filter(file => file.type === "application/pdf"));
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
        <div className="max-w-3xl mx-auto mt-10 p-8 bg-white rounded-xl shadow-lg border border-blue-200">
            <h1 className="text-4xl font-bold mb-6 text-center text-blue-600">Upload Resumes and Job Description</h1>
            <form onSubmit={handleSubmit} className="space-y-8">
                <div>
                    <label className="block text-lg font-semibold text-blue-700 mb-3">Select Folder (PDFs only):</label>
                    <input 
                        type="file"
                        webkitdirectory="true"
                        directory="true"
                        onChange={handleFolderChange}
                        multiple
                        className="block w-full text-sm text-gray-600 border border-blue-200 rounded-md cursor-pointer bg-blue-50 hover:bg-blue-100 focus:outline-none focus:ring-2 focus:ring-blue-400"
                    />
                </div>
                <div>
                    <label className="block text-lg font-semibold text-blue-700 mb-3">Job Description:</label>
                    <textarea
                        value={jobDescription}
                        onChange={handleJobDescriptionChange}
                        placeholder="Enter the job description here"
                        rows="5"
                        className="w-full p-4 border border-blue-200 rounded-md bg-blue-50 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-400 hover:bg-blue-100"
                    />
                </div>
                <div className="flex flex-col space-y-4 sm:space-y-0 sm:flex-row sm:space-x-4">
                    <button 
                        type="submit" 
                        className="w-full py-3 bg-blue-500 text-white font-semibold rounded-md hover:bg-blue-600 transition-colors"
                    >
                        Submit
                    </button>
                    <button 
                        type="button" 
                        onClick={handleReset}
                        className="w-full py-3 bg-red-500 text-white font-semibold rounded-md hover:bg-red-600 transition-colors"
                    >
                        Reset Uploads
                    </button>
                </div>
            </form>
            {responseMessage && (
                <p className="mt-6 text-center text-lg text-blue-700 font-medium">{responseMessage}</p>
            )}
        </div>
    );
};

export default ResumeUploader;
