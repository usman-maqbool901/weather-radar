export interface ApiError {
  error: string;
  message: string;
}

export interface ApiResponse<T> {
  data?: T;
  error?: ApiError;
}

import type { RadarData } from './radar';

export interface RadarResponse {
  data: RadarData;
  lastUpdated: string;
  dataTimestamp: string;
}

