import { useEffect, useRef, useState } from 'react';
import 'mapbox-gl/dist/mapbox-gl.css';
import type * as mapboxgl from 'mapbox-gl';
import { initMapbox } from '../lib/mapbox';
import { RADAR_COLORS } from '../utils/constants';
import type { RadarData } from '../types/radar';

interface RadarMapProps {
  data: RadarData | null;
  mapboxToken: string;
}

const RadarMap = ({ data, mapboxToken }: RadarMapProps) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<mapboxgl.Map | null>(null);
  const [mapLoaded, setMapLoaded] = useState(false);

  useEffect(() => {
    if (!mapContainer.current || map.current) return;

    map.current = initMapbox(mapContainer.current, mapboxToken);

    map.current.on('load', () => {
      setMapLoaded(true);
    });

    map.current.on('error', (e) => {
      console.error('Mapbox error:', e);
      if (e.error?.message?.includes('Forbidden') || e.error?.message?.includes('401') || e.error?.message?.includes('403')) {
        console.error('Mapbox token error: Token may have URL restrictions or missing scopes. Check MAPBOX_TOKEN_SETUP.md');
      }
    });

    return () => {
      if (map.current) {
        map.current.remove();
        map.current = null;
      }
    };
  }, [mapboxToken]);

  useEffect(() => {
    if (!map.current || !mapLoaded || !data || !data.features || data.features.length === 0) {
      return;
    }

    const sourceId = 'radar-data';
    const layerId = 'radar-heatmap';

    const setupLayer = () => {
      if (!map.current) return;

      try {
        // Calculate bounds from data
        const coordinates = data.features.map(f => f.geometry.coordinates);
        const lons = coordinates.map(c => c[0]);
        const lats = coordinates.map(c => c[1]);
        const bounds = [
          [Math.min(...lons), Math.min(...lats)],
          [Math.max(...lons), Math.max(...lats)]
        ] as [[number, number], [number, number]];

        // Add or update source
        if (map.current.getSource(sourceId)) {
          const source = map.current.getSource(sourceId) as mapboxgl.GeoJSONSource;
          source.setData(data);
        } else {
          map.current.addSource(sourceId, {
            type: 'geojson',
            data: data,
          });
        }

        // Remove existing layer if present
        if (map.current.getLayer(layerId)) {
          map.current.removeLayer(layerId);
        }

        // Add circle layer
        map.current.addLayer({
          id: layerId,
          type: 'circle',
          source: sourceId,
          paint: {
            'circle-radius': [
              'interpolate',
              ['linear'],
              ['zoom'],
              0,
              2,
              5,
              4,
              10,
              8,
            ],
            'circle-color': [
              'interpolate',
              ['linear'],
              ['get', 'reflectivity'],
              ...RADAR_COLORS.flat(),
            ],
            'circle-opacity': [
              'interpolate',
              ['linear'],
              ['get', 'reflectivity'],
              -10,
              0.3,
              0,
              0.4,
              10,
              0.5,
              20,
              0.6,
              30,
              0.7,
              40,
              0.8,
              50,
              0.9,
              60,
              1,
            ],
            'circle-stroke-width': 0,
            'circle-blur': [
              'interpolate',
              ['linear'],
              ['zoom'],
              0,
              0.5,
              5,
              1,
              10,
              2,
            ],
          },
        });

        // Fit map to data bounds with padding
        map.current.fitBounds(bounds, {
          padding: { top: 50, bottom: 50, left: 50, right: 50 },
          maxZoom: 8,
        });
      } catch (error) {
        console.error('Error setting up radar layer:', error);
      }
    };

    if (map.current.isStyleLoaded()) {
      setTimeout(setupLayer, 200);
    } else {
      map.current.once('styledata', () => {
        setTimeout(setupLayer, 200);
      });
    }
  }, [map, mapLoaded, data]);

  return (
    <div className="relative w-full h-full">
      <div ref={mapContainer} className="w-full h-full rounded-lg overflow-hidden" />
      {!mapLoaded && (
        <div className="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-slate-100 to-slate-200">
          <div className="text-center space-y-4">
            <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-200 border-t-blue-600 mx-auto"></div>
            <p className="text-slate-700 font-medium">Loading map...</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default RadarMap;
