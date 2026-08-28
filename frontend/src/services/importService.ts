import { UploadResponse } from "../types/upload.types";
import apiService from "./api";

class ImportService {
  async uploadWords(file: File): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await apiService
      .getApiInstance()
      .post<UploadResponse>("/upload/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
    return response.data;
  }
}

export default new ImportService();
