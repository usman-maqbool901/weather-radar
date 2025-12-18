import { useState, useEffect } from 'react';
import { fetchRadarData } from '../lib/api';
import type { RadarResponse, ApiError } from '../types/api';

interface UseRadarDataReturn {
  data: RadarResponse | null;
  loading: boolean;
  error: ApiError | null;
  refetch: () => Promise<void>;
}

export const useRadarData = (autoRefresh = false): UseRadarDataReturn => {
  const [data, setData] = useState<RadarResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<ApiError | null>(null);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetchRadarData();
      setData(response);
    } catch (err) {
      setError(err as ApiError);
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();

    if (autoRefresh) {
      const interval = setInterval(loadData, 60000);
      return () => clearInterval(interval);
    }
  }, [autoRefresh]);

  return {
    data,
    loading,
    error,
    refetch: loadData,
  };
};

