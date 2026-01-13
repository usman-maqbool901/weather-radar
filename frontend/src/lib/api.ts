import axios from 'axios';
import type { RadarResponse, ApiError } from '../types/api';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

export const fetchRadarData = async (): Promise<RadarResponse> => {
  try {
    const response = await apiClient.get<RadarResponse>('/api/radar/latest');
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw {
        error: error.response?.data?.error || 'Network Error',
        message: error.response?.data?.message || error.message,
      } as ApiError;
    }
    throw {
      error: 'Unknown Error',
      message: 'An unexpected error occurred',
    } as ApiError;
  }
};

