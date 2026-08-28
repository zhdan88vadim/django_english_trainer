import apiService from './api';
import { Category, CategoryApiResponse } from '../types/index';

class CategoryService {

  async fetchCategories(): Promise<Category[]> {
    const response = await apiService.getApiInstance().get<CategoryApiResponse>('/categories/');
    return response.data.results;
  }

  async getCategoryWords(categoryId: number): Promise<any> {
    const response = await apiService.getApiInstance().get(`/categories/${categoryId}/words/`);
    return response.data;
  }

}

export default new CategoryService();