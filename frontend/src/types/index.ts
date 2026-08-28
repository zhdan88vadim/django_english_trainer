// Existing types
export interface Word {
  id: number;
  word: string;
  translation: string;
  description: string;
  created_at: string;
}

export interface Category {
  id: number;
  name: string;
  word_count?: number;
  created_at?: string;
  updated_at?: string;
}

export interface CategoryApiResponse {
  results: Category[];
  total: number;
  page: number;
  has_more: boolean;
}

export interface ApiResponse {
  results: Word[];
  total: number;
  page: number;
  has_more: boolean;
}

export interface ApiError {
  message: string;
  status?: number;
  data?: any;
}

export interface AppState {
  words: Word[];
  currentIndex: number;
  currentPage: number;
  hasMore: boolean;
  isLoading: boolean;
  isRevealed: boolean;
  total: number;
  error: string | null;
}

// NEW: Auth types
export interface User {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  is_verified: boolean;
  date_joined?: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password1: string;
  password2: string;
  username?: string;
  first_name?: string;
  last_name?: string;
}

export interface AuthResponse {
  key: string;
  user: User;
}

export interface PasswordChangeData {
  old_password: string;
  new_password1: string;
  new_password2: string;
}