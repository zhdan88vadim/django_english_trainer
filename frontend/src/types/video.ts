export interface TaskResponse {
  status: string;
  task_id: string;
  message: string;
}

export interface TaskStatus {
  status: 'pending' | 'processing' | 'completed' | 'failed'; 
  progress: number;
  message: string;
  output: string;
}

export interface GenerateVideoRequest {
  text: string;
}