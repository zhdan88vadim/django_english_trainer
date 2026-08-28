// components/FileUpload.tsx
import React, { useRef, DragEvent, ChangeEvent } from 'react';
import { useFileUpload } from './hooks/useFileUpload';
import './FileUpload.scss';

interface FileUploadProps {
  accept?: string;
  maxSize?: number; // in bytes
  onUploadSuccess?: (response: any) => void;
  onUploadError?: (error: string) => void;
  className?: string;
}

const FileUpload: React.FC<FileUploadProps> = ({
  accept = '.csv,.xlsx,.xls,.txt',
  maxSize = 5 * 1024 * 1024, // 5MB default
  onUploadSuccess,
  onUploadError,
  className = '',
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const {
    file,
    fileInfo,
    uploading,
    progress,
    message,
    isSuccess,
    isError,
    response,
    preview,
    uploadFile,
    setFile,
    resetUpload,
  } = useFileUpload();

  const handleFileSelect = (event: ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      validateAndSetFile(selectedFile);
    }
  };

  const validateAndSetFile = (selectedFile: File) => {
    // Validate file size
    if (selectedFile.size > maxSize) {
      const maxSizeMB = (maxSize / (1024 * 1024)).toFixed(1);
      alert(`File too large. Maximum size is ${maxSizeMB}MB.`);
      return;
    }

    // Validate file type
    const acceptedTypes = accept.split(',').map(type => type.trim());
    const fileExtension = `.${selectedFile.name.split('.').pop()?.toLowerCase()}`;
    
    if (!acceptedTypes.includes(fileExtension) && 
        !acceptedTypes.includes(selectedFile.type)) {
      alert(`File type not accepted. Please upload: ${accept}`);
      return;
    }

    setFile(selectedFile);
  };

  const handleDragOver = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.stopPropagation();
    event.currentTarget.classList.add('drag-over');
  };

  const handleDragLeave = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.stopPropagation();
    event.currentTarget.classList.remove('drag-over');
  };

  const handleDrop = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.stopPropagation();
    event.currentTarget.classList.remove('drag-over');

    const droppedFile = event.dataTransfer.files?.[0];
    if (droppedFile) {
      validateAndSetFile(droppedFile);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file first');
      return;
    }

    const result = await uploadFile(file);
    
    if (result && onUploadSuccess) {
      onUploadSuccess(result);
    } else if (!result && onUploadError) {
      onUploadError('Upload failed');
    }
  };

  const handleReset = () => {
    resetUpload();
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className={`file-upload-container ${className}`}>
      <div
        className={`drop-zone ${uploading ? 'uploading' : ''} ${isSuccess ? 'success' : ''} ${isError ? 'error' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !uploading && fileInputRef.current?.click()}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept={accept}
          onChange={handleFileSelect}
          disabled={uploading}
          style={{ display: 'none' }}
        />

        {!file && !uploading && (
          <div className="upload-prompt">
            <div className="upload-icon">📁</div>
            <h3>Drag & drop your file here</h3>
            <p>or click to browse</p>
            <p className="file-types">Supported: {accept}</p>
          </div>
        )}

        {file && !uploading && (
          <div className="file-info">
            <div className="file-icon">📄</div>
            <div className="file-details">
              <h4>{file.name}</h4>
              <p>{formatFileSize(file.size)}</p>
            </div>
            <button
              className="remove-file"
              onClick={(e) => {
                e.stopPropagation();
                handleReset();
              }}
            >
              ✕
            </button>
          </div>
        )}

        {uploading && (
          <div className="upload-progress">
            <div className="progress-bar-container">
              <div
                className="progress-bar"
                style={{ width: `${progress}%` }}
              >
                {progress > 5 && `${progress}%`}
              </div>
            </div>
            <p>Uploading... {progress}%</p>
          </div>
        )}

        {isSuccess && response && (
          <div className="upload-result success">
            <div className="result-icon">✅</div>
            <div className="result-details">
              <h4>Upload Successful!</h4>
              <p>{response.message}</p>
              <p>Records processed: {response.records_processed}</p>
            </div>
          </div>
        )}

        {isError && (
          <div className="upload-result error">
            <div className="result-icon">❌</div>
            <div className="result-details">
              <h4>Upload Failed</h4>
              <p>{message}</p>
            </div>
          </div>
        )}
      </div>

      {file && !uploading && !isSuccess && !isError && (
        <div className="upload-actions">
          <button
            className="btn btn-upload"
            onClick={handleUpload}
            disabled={uploading}
          >
            Upload File
          </button>
          <button
            className="btn btn-cancel"
            onClick={handleReset}
            disabled={uploading}
          >
            Cancel
          </button>
        </div>
      )}

      {isSuccess && (
        <button
          className="btn btn-upload-more"
          onClick={handleReset}
        >
          Upload Another File
        </button>
      )}

      {preview && preview.length > 0 && (
        <div className="data-preview">
          <h4>Data Preview</h4>
          <div className="preview-table-container">
            <table className="preview-table">
              <thead>
                <tr>
                  {Object.keys(preview[0] || {}).map((key) => (
                    <th key={key}>{key}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {preview.map((row, index) => (
                  <tr key={index}>
                    {Object.values(row).map((value: any, colIndex) => (
                      <td key={colIndex}>
                        {typeof value === 'object' 
                          ? JSON.stringify(value) 
                          : String(value)
                        }
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {message && !isSuccess && !isError && (
        <div className="status-message">{message}</div>
      )}
    </div>
  );
};

export default FileUpload;