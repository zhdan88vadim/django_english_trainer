import axios, { AxiosInstance, AxiosError } from 'axios';
import { 
  Word, 
  ApiResponse, 
  ApiError, 
  User, 
  LoginCredentials, 
  RegisterData,
  AuthResponse,
  PasswordChangeData
} from '../types';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8090/api',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor for authentication
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('token');
        if (token) {
          config.headers.Authorization = `Token ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor for error handling
    this.api.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        // Handle 401 Unauthorized
        if (error.response?.status === 401) {
          const token = localStorage.getItem('token');
          if (token) {
            // Token expired or invalid
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            // Redirect to login if not already there
            if (!window.location.pathname.includes('/login')) {
              window.location.href = '/login';
            }
          }
        }

        const apiError: ApiError = {
          message: error.message,
          status: error.response?.status,
          data: error.response?.data,
        };
        return Promise.reject(apiError);
      }
    );
  }

  getApiInstance(): AxiosInstance {
    return this.api;
  }

  // ============ AUTH ENDPOINTS ============
  
  /**
   * Login user
   */
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await this.api.post<AuthResponse>('/auth/login/', credentials);
    // Store token and user
    localStorage.setItem('token', response.data.key);
    localStorage.setItem('user', JSON.stringify(response.data.user));
    return response.data;
  }

  /**
   * Register user
   */
  async register(data: RegisterData): Promise<AuthResponse> {
    const response = await this.api.post<AuthResponse>('/auth/register/', data);
    // Store token and user
    localStorage.setItem('token', response.data.key);
    localStorage.setItem('user', JSON.stringify(response.data.user));
    return response.data;
  }

  /**
   * Logout user
   */
  async logout(): Promise<void> {
    try {
      await this.api.post('/auth/logout/');
    } catch (error) {
      // Ignore errors on logout
    } finally {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    }
  }

  /**
   * Get current user
   */
  async getCurrentUser(): Promise<User> {
    const response = await this.api.get<User>('/auth/user/');
    localStorage.setItem('user', JSON.stringify(response.data));
    return response.data;
  }

  /**
   * Update user profile
   */
  async updateUser(data: Partial<User>): Promise<User> {
    const response = await this.api.put<User>('/auth/user/update/', data);
    localStorage.setItem('user', JSON.stringify(response.data));
    return response.data;
  }

  /**
   * Change password
   */
  async changePassword(data: PasswordChangeData): Promise<any> {
    const response = await this.api.post('/auth/password/change/', data);
    // If token is returned, update it
    if (response.data.key) {
      localStorage.setItem('token', response.data.key);
    }
    return response.data;
  }

  /**
   * Request password reset
   */
  async requestPasswordReset(email: string): Promise<any> {
    const response = await this.api.post('/auth/password/reset/', { email });
    return response.data;
  }

  /**
   * Confirm password reset
   */
  async confirmPasswordReset(
    uid: string, 
    token: string, 
    newPassword1: string, 
    newPassword2: string
  ): Promise<any> {
    const response = await this.api.post('/auth/password/reset/confirm/', {
      uid,
      token,
      new_password1: newPassword1,
      new_password2: newPassword2,
    });
    return response.data;
  }

  /**
   * Verify email
   */
  async verifyEmail(key: string): Promise<any> {
    const response = await this.api.post('/auth/registration/verify-email/', { key });
    return response.data;
  }

  /**
   * Resend verification email
   */
  async resendVerificationEmail(email: string): Promise<any> {
    const response = await this.api.post('/auth/registration/resend-email/', { email });
    return response.data;
  }

  // ============ YOUR EXISTING WORD ENDPOINTS ============
  
  /**
   * Fetch words with pagination
   */
  async fetchWords(page: number = 1, limit: number): Promise<ApiResponse> {
    const response = await this.api.get<ApiResponse>('/words/', {
      params: { page, limit },
    });
    return response.data;
  }

  async fetchRandomWords(count: number, categoryId?: number | null): Promise<ApiResponse> {
    const response = await this.api.get<ApiResponse>('/words/random/', {
      params: { count, category_id: categoryId },
    });
    return response.data;
  }

  /**
   * Create a new word
   */
  async createWord(word: string, translation: string): Promise<Word> {
    const response = await this.api.post<Word>('/words/', { word, translation });
    return response.data;
  }

  /**
   * Delete a word
   */
  async deleteWord(id: number): Promise<void> {
    await this.api.delete(`/words/${id}/`);
  }

  /**
   * Update a word
   */
  async updateWord(id: number, word: string, translation: string): Promise<Word> {
    const response = await this.api.put<Word>(`/words/${id}/`, { word, translation });
    return response.data;
  }

  /**
   * Search words
   */
  async searchWords(query: string): Promise<Word[]> {
    const response = await this.api.get<Word[]>('/words/search/', {
      params: { q: query },
    });
    return response.data;
  }

  // ============ HELPER METHODS ============
  
  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    const token = localStorage.getItem('token');
    return !!token;
  }

  /**
   * Get stored user
   */
  getStoredUser(): User | null {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      try {
        return JSON.parse(userStr);
      } catch {
        return null;
      }
    }
    return null;
  }

  /**
   * Get auth token
   */
  getToken(): string | null {
    return localStorage.getItem('token');
  }

  /**
   * Clear all auth data
   */
  clearAuth(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }
}

export default new ApiService();