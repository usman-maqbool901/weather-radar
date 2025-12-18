export const RADAR_COLORS = [
  [-10, 'rgba(0, 50, 200, 0.2)'],
  [0, 'rgba(0, 0, 255, 0.3)'],
  [5, 'rgba(0, 100, 255, 0.5)'],
  [10, 'rgba(0, 150, 255, 0.7)'],
  [15, 'rgba(0, 200, 255, 0.8)'],
  [20, 'rgba(100, 255, 255, 0.9)'],
  [25, 'rgba(150, 255, 200, 0.9)'],
  [30, 'rgba(200, 255, 150, 0.9)'],
  [35, 'rgba(255, 255, 100, 1)'],
  [40, 'rgba(255, 200, 0, 1)'],
  [45, 'rgba(255, 150, 0, 1)'],
  [50, 'rgba(255, 100, 0, 1)'],
  [55, 'rgba(255, 50, 0, 1)'],
  [60, 'rgba(255, 0, 0, 1)'],
  [65, 'rgba(200, 0, 100, 1)'],
  [70, 'rgba(150, 0, 150, 1)'],
] as const;

export const DBZ_RANGES = [
  { min: -10, max: 5, label: '< 5', color: 'rgba(0, 0, 255, 0.3)' },
  { min: 5, max: 10, label: '5-10', color: 'rgba(0, 100, 255, 0.5)' },
  { min: 10, max: 15, label: '10-15', color: 'rgba(0, 150, 255, 0.7)' },
  { min: 15, max: 20, label: '15-20', color: 'rgba(100, 255, 255, 0.8)' },
  { min: 20, max: 25, label: '20-25', color: 'rgba(150, 255, 200, 0.9)' },
  { min: 25, max: 30, label: '25-30', color: 'rgba(200, 255, 150, 0.9)' },
  { min: 30, max: 35, label: '30-35', color: 'rgba(255, 255, 100, 1)' },
  { min: 35, max: 40, label: '35-40', color: 'rgba(255, 200, 0, 1)' },
  { min: 40, max: 45, label: '40-45', color: 'rgba(255, 150, 0, 1)' },
  { min: 45, max: 50, label: '45-50', color: 'rgba(255, 100, 0, 1)' },
  { min: 50, max: 55, label: '50-55', color: 'rgba(255, 50, 0, 1)' },
  { min: 55, max: 60, label: '55-60', color: 'rgba(255, 0, 0, 1)' },
  { min: 60, max: 65, label: '60-65', color: 'rgba(200, 0, 100, 1)' },
  { min: 65, max: 75, label: '65+', color: 'rgba(150, 0, 150, 1)' },
] as const;

export const MAP_CONFIG = {
  defaultCenter: [-95.7129, 37.0902] as [number, number],
  defaultZoom: 4,
  minZoom: 2,
  maxZoom: 10,
  style: 'mapbox://styles/mapbox/dark-v11',
} as const;

