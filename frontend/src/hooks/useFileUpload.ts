// hooks/useFileUpload.ts
import { useState, useCallback } from 'react';
import axios, { AxiosProgressEvent } from 'axios';
import { UploadState, UploadResponse, UploadError } from '../types/upload.types';
import importService from '../services/importService';

const API_BASE_URL = 'http://192.168.0.254:8090';

export const useFileUpload = () => {
  const [state, setState] = useState<UploadState>({
    file: null,
    fileInfo: null,
    uploading: false,
    progress: 0,
    message: '',
    isSuccess: false,
    isError: false,
    response: null,
    preview: null,
  });

  const getCookie = useCallback((name: string): string | null => {
    if (typeof document === 'undefined') return null;
    
    const cookieValue = document.cookie
      .split('; ')
      .find(row => row.startsWith(`${name}=`))
      ?.split('=')[1];
    
    return cookieValue ? decodeURIComponent(cookieValue) : null;
  }, []);

  const resetUpload = useCallback(() => {
    setState(prev => ({
      ...prev,
      file: null,
      fileInfo: null,
      progress: 0,
      message: '',
      isSuccess: false,
      isError: false,
      response: null,
      preview: null,
    }));
  }, []);

  const uploadFile = useCallback(async (file: File): Promise<UploadResponse | null> => {
    if (!file) {
      setState(prev => ({
        ...prev,
        message: 'Please select a file first',
        isError: true,
      }));
      return null;
    }

    setState(prev => ({
      ...prev,
      uploading: true,
      progress: 0,
      message: 'Uploading...',
      isSuccess: false,
      isError: false,
      file,
      fileInfo: {
        name: file.name,
        size: file.size,
        type: file.type,
        lastModified: file.lastModified,
      },
    }));

    try {
      const data = await importService.uploadWords(file)

      setState(prev => ({
        ...prev,
        uploading: false,
        progress: 100,
        message: '✅ File uploaded successfully!',
        isSuccess: true,
        isError: false,
        response: data,
        preview: data.data_preview || null,
      }));

      return data;

    } catch (error) {
      let errorMessage = 'Upload failed';
      
      if (axios.isAxiosError(error)) {
        const errorData = error.response?.data as UploadError;
        errorMessage = errorData?.error || error.message || 'Upload failed';
        
        if (error.response?.status === 403) {
          errorMessage = 'Authentication failed. Please log in again.';
        } else if (error.response?.status === 413) {
          errorMessage = 'File too large. Maximum size is 5MB.';
        }
      }

      setState(prev => ({
        ...prev,
        uploading: false,
        progress: 0,
        message: `❌ ${errorMessage}`,
        isSuccess: false,
        isError: true,
        response: null,
      }));

      return null;
    }
  }, [getCookie]);

  const setFile = useCallback((file: File | null) => {
    setState(prev => ({
      ...prev,
      file,
      fileInfo: file ? {
        name: file.name,
        size: file.size,
        type: file.type,
        lastModified: file.lastModified,
      } : null,
      message: file ? `Selected: ${file.name}` : '',
      isSuccess: false,
      isError: false,
    }));
  }, []);

  return {
    ...state,
    uploadFile,
    setFile,
    resetUpload,
  };
};