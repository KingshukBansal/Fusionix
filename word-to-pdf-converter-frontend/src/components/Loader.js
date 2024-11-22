import React from 'react';

const Loader = () => {
  return (
    <div className="flex justify-center items-center space-x-2 mt-4">
      <div className="w-6 h-6 border-4 border-indigo-500 border-t-transparent border-solid rounded-full animate-spin"></div>
      <span className="text-white">Uploading...</span>
    </div>
  );
};

export default Loader;
