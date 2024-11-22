import React from 'react';

const MetadataDisplay = ({ metadata }) => {
  // Function to render metadata as key-value pairs
  const renderMetadata = (data) => {
    return Object.keys(data).map((key) => (
      <div key={key} className="grid grid-cols-2 gap-2 mb-3"> {/* Reduced gap from 4 to 2 */}
        <span className="font-medium text-indigo-400">{key}:</span>
        <span className="text-white break-words">{data[key]}</span>
      </div>
    ));
  };

  return (
    <div className="bg-gray-800 p-6 rounded-lg mt-6 shadow-lg">
      <h3 className="text-xl font-semibold text-indigo-500">File Metadata</h3>
      <div className="mt-4">
        {metadata ? (
          <div className="space-y-2">
            {renderMetadata(metadata)} {/* Render metadata key-value pairs */}
          </div>
        ) : (
          <p className="text-white">No metadata available.</p>
        )}
      </div>
    </div>
  );
};

export default MetadataDisplay;
