export interface UploadResponse {
  message: string;
  filename: string;
  records_processed: number;
  data_preview?: any[];
  error?: string;
}

export interface UploadError {
  error: string;
  [key: string]: any;
}

export interface FileInfo {
  name: string;
  size: number;
  type: string;
  lastModified: number;
}

export interface UploadState {
  file: File | null;
  fileInfo: FileInfo | null;
  uploading: boolean;
  progress: number;
  message: string;
  isSuccess: boolean;
  isError: boolean;
  response: UploadResponse | null;
  preview: any[] | null;
}