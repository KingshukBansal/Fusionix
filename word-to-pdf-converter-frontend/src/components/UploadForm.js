import React, { useState } from 'react';

const UploadForm = ({ onUpload }) => {
  const [useEmail, setUseEmail] = useState(false);
  const [usePassword, setUsePassword] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (file) {
      onUpload(useEmail ? email : '', file, usePassword ? password : '');
    }
  };

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-md">
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="file" className="block text-sm font-medium text-white">
            Choose File
          </label>
          <input
            type="file"
            id="file"
            onChange={handleFileChange}
            required
            className="mt-1 block w-full text-sm text-white file:bg-gray-700 file:text-white file:py-2 file:px-4 file:rounded-md"
          />
        </div>

        <div className="flex items-center mb-4 space-x-6">
          {/* Email Checkbox */}
          <label htmlFor="useEmail" className="flex items-center text-sm font-medium text-white">
            <input
              type="checkbox"
              id="useEmail"
              checked={useEmail}
              onChange={() => setUseEmail(!useEmail)}
              className="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
            />
            <span className="ml-2">Add Email</span>
          </label>

          {/* Password Checkbox */}
          <label htmlFor="usePassword" className="flex items-center text-sm font-medium text-white">
            <input
              type="checkbox"
              id="usePassword"
              checked={usePassword}
              onChange={() => setUsePassword(!usePassword)}
              className="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
            />
            <span className="ml-2">Password Protect PDF</span>
          </label>
        </div>

        {useEmail && (
          <div className="mb-4">
            <label htmlFor="email" className="block text-sm font-medium text-white">
              Email
            </label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-1 block w-full px-4 py-2 bg-gray-700 text-white rounded-md"
            />
          </div>
        )}

        {usePassword && (
          <div className="mb-4">
            <label htmlFor="password" className="block text-sm font-medium text-white">
              Password
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 block w-full px-4 py-2 bg-gray-700 text-white rounded-md"
            />
          </div>
        )}

        <button
          type="submit"
          className="w-full bg-indigo-600 text-white py-2 rounded-md hover:bg-indigo-700 transition duration-200"
        >
          Upload
        </button>
      </form>
    </div>
  );
};

export default UploadForm;
