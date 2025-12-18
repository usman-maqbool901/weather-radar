export interface RadarPoint {
  type: 'Feature';
  geometry: {
    type: 'Point';
    coordinates: [number, number];
  };
  properties: {
    reflectivity: number;
  };
}

export interface RadarData {
  type: 'FeatureCollection';
  features: RadarPoint[];
}

export interface RadarMetadata {
  lastUpdated: string;
  dataTimestamp: string;
}

export interface RadarResponse {
  data: RadarData;
  lastUpdated: string;
  dataTimestamp: string;
}

