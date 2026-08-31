import { TaskResponse, TaskStatus } from '../types/video';
import apiService from './api';

class VideoService {
  
  async generateVideo(file: File): Promise<TaskResponse> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await apiService
      .getApiInstance()
      .post<TaskResponse>("/generate-video/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
    return response.data;
  }

  async getTaskStatus(taskId: string): Promise<TaskStatus> {
    const response = await apiService
      .getApiInstance()
      .get<TaskStatus>(`/task-status/${taskId}/`);
    return response.data;
  }

  getDownloadUrl(outputPath: string): string {
    const baseURL = apiService.getApiInstance().defaults.baseURL || '';
    return `${baseURL}/download/${encodeURIComponent(outputPath)}/`;
  }

  // If you need to generate video from text (instead of file)
  async generateVideoFromText(text: string): Promise<TaskResponse> {
    const response = await apiService
      .getApiInstance()
      .post<TaskResponse>("/generate_video_from_csv/", { text });
    return response.data;
  }
}

export default new VideoService();