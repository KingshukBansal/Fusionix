import React, { useState } from 'react';

const UploadForm = ({ onUpload }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [file, setFile] = useState(null);
  const [usePassword, setUsePassword] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleCheckboxChange = () => {
    setUsePassword(!usePassword);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (file) {
      onUpload(email, file, usePassword ? password : '');
    }
  };

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-md">
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="email" className="block text-sm font-medium text-white">Email</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="mt-1 block w-full px-4 py-2 bg-gray-700 text-white rounded-md"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="file" className="block text-sm font-medium text-white">Choose File</label>
          <input
            type="file"
            id="file"
            onChange={handleFileChange}
            required
            className="mt-1 block w-full text-sm text-white file:bg-gray-700 file:text-white file:py-2 file:px-4 file:rounded-md"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="password" className="inline-flex items-center text-sm font-medium text-white">
            <input
              type="checkbox"
              id="usePassword"
              checked={usePassword}
              onChange={handleCheckboxChange}
              className="mr-2"
            />
            Password Protect PDF
          </label>
          {usePassword && (
            <input
              type="password"
              id="password"
              value={password}
              onChange={handlePasswordChange}
              className="mt-1 block w-full px-4 py-2 bg-gray-700 text-white rounded-md"
            />
          )}
        </div>

        <button
          type="submit"
          className="w-full bg-indigo-600 text-white py-2 rounded-md hover:bg-indigo-700"
        >
          Upload
        </button>
      </form>
    </div>
  );
};

export default UploadForm;
