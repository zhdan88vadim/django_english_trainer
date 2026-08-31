import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ProtectedRoute } from './components/common/ProtectedRoute';
import { Login } from './components/auth/Login';
import { Register } from './components/auth/Register';
import Home from './Home'; // Your main component with words
import './App.scss';
import Categories from './Categories';
import FileUpload from './FileUpload';
import { VideoGenerator } from './components/VideoGenerator';

const App: React.FC = () => {
  const handleUploadSuccess = (response: any) => {
    console.log('Upload successful:', response);
    // You can show a notification, update state, etc.
  };

  const handleUploadError = (error: string) => {
    console.error('Upload error:', error);
    // Handle error appropriately
  };
  

  return (
    <AuthProvider>
      <Router>
        <div className="app">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route 
              path="/" 
              element={
                <ProtectedRoute>
                  <Home />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/generate" 
              element={
                <ProtectedRoute>
                  <VideoGenerator />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/categories" 
              element={
                <ProtectedRoute>
                  <Categories />
                </ProtectedRoute>
              } 
            />            
            <Route 
              path="/upload" 
              element={
                <ProtectedRoute>
                  <FileUpload
                      accept=".csv,.xlsx,.xls,.txt"
                      maxSize={5 * 1024 * 1024} // 5MB
                      onUploadSuccess={handleUploadSuccess}
                      onUploadError={handleUploadError}
                    />
                </ProtectedRoute>
              } 
            />            
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
};

export default App;