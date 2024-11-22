import React from 'react';

const DownloadButton = ({ onDownload, isDownloading, downloadError }) => {
  return (
    <div className="mt-6">
      {downloadError ? (
        <p className="text-red-500">Download failed, retrying...</p>
      ) : isDownloading ? (
        <button className="w-full bg-indigo-600 text-white py-2 rounded-md cursor-not-allowed">Downloading...</button>
      ) : (
        <button
          onClick={onDownload}
          className="w-full bg-green-600 text-white py-2 rounded-md hover:bg-green-700"
        >
          Download PDF
        </button>
      )}
    </div>
  );
};

export default DownloadButton;
