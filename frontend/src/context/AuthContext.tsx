import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import apiService from '../services/api';
import { User, LoginCredentials, RegisterData, PasswordChangeData } from '../types';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  updateUser: (data: Partial<User>) => Promise<void>;
  changePassword: (data: PasswordChangeData) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(apiService.getStoredUser());
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const token = apiService.getToken();
      if (token) {
        try {
          // Verify token by getting current user
          const userData = await apiService.getCurrentUser();
          setUser(userData);
        } catch (error) {
          // Token invalid or expired
          apiService.clearAuth();
          setUser(null);
        }
      }
      setIsLoading(false);
    };

    initAuth();
  }, []);

  const login = async (credentials: LoginCredentials) => {
    const data = await apiService.login(credentials);
    setUser(data.user);
  };

  const register = async (data: RegisterData) => {
    const response = await apiService.register(data);
    setUser(response.user);
  };

  const logout = async () => {
    await apiService.logout();
    setUser(null);
  };

  const updateUser = async (data: Partial<User>) => {
    const updatedUser = await apiService.updateUser(data);
    setUser(updatedUser);
  };

  const changePassword = async (data: PasswordChangeData) => {
    await apiService.changePassword(data);
  };

  const value = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    logout,
    updateUser,
    changePassword,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};