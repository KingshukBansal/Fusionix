import React, { useState } from 'react';
import axios from 'axios';
import UploadForm from './components/UploadForm';
import MetadataDisplay from './components/MetadataDisplay';
import DownloadButton from './components/DownloadButton';
import Loader from './components/Loader';

function App() {
  const [docxFid, setDocxFid] = useState(null);
  const [metadata, setMetadata] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isDownloading, setIsDownloading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState('');
  const [downloadError, setDownloadError] = useState(false);

  // Handle file upload
  const handleUpload = async (email, file, password) => {
    setIsUploading(true);
    setUploadMessage('');
    try {
      const formData = new FormData();
      formData.append('email', email);
      formData.append('file', file);
      if (password) formData.append('password', password);

      const response = await axios.post(`${process.env.REACT_APP_API_BASE_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setDocxFid(response.data.docx_id);
      setUploadMessage('File uploaded successfully!');

      // Fetch metadata after upload
      await fetchMetadata(response.data.docx_id);
    } catch (error) {
      console.error('Upload failed', error);
      setUploadMessage('File upload failed. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  // Fetch metadata using docx_fid
  const fetchMetadata = async (docxFid) => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/getMetadata?fid=${docxFid}`);
      setMetadata(response.data);
    } catch (error) {
      console.error('Metadata fetch failed', error);
      setMetadata(null); // In case of failure, we clear previous metadata
    }
  };

  // Handle file download
  const handleDownload = async () => {
    setIsDownloading(true);
    setDownloadError(false);
    try {
      const response = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/download?fid=${docxFid}`, {
        responseType: 'blob', // Important for file download
      });
      
      // Create a downloadable link for the file
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'converted-file.pdf');
      link.click();
    } catch (error) {
      setDownloadError(true);
      setTimeout(handleDownload, 5000); // Retry after 5 seconds if failed
    } finally {
      setIsDownloading(false);
    }
  };

  return (
    <div className="container mx-auto p-4 dark:bg-gray-900 dark:text-white min-h-screen max-w-screen-lg">
      {/* Updated File Upload Heading */}
      <h2 className="text-3xl text-center font-semibold text-indigo-400 mb-6 sm:text-2xl md:text-3xl lg:text-4xl xl:text-5xl">
        DOCX to PDF Converter
      </h2>

      <UploadForm onUpload={handleUpload} />
      
      {/* Display upload success message */}
      {uploadMessage && <div className="mt-4 text-white">{uploadMessage}</div>}
      
      {isUploading && <Loader />}
      {metadata && <MetadataDisplay metadata={metadata} />}
      {docxFid && !isUploading && <DownloadButton onDownload={handleDownload} isDownloading={isDownloading} downloadError={downloadError} />}
    </div>
  );
}

export default App;
