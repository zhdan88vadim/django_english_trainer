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

export interface AuthContextType {
    user: User | null;
    token: string | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    login: (credentials: LoginCredentials) => Promise<void>;
    register: (data: RegisterData) => Promise<void>;
    logout: () => Promise<void>;
    updateUser: (data: Partial<User>) => Promise<void>;
    changePassword: (oldPassword: string, newPassword1: string, newPassword2: string) => Promise<void>;
}