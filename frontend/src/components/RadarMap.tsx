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
        if (map.current.getSource(sourceId)) {
          const source = map.current.getSource(sourceId) as mapboxgl.GeoJSONSource;
          source.setData(data);
        } else {
          map.current.addSource(sourceId, {
            type: 'geojson',
            data: data,
          });
        }

        if (map.current.getLayer(layerId)) {
          map.current.removeLayer(layerId);
        }

        map.current.addLayer({
          id: layerId,
          type: 'heatmap',
          source: sourceId,
          paint: {
            'heatmap-weight': [
              'interpolate',
              ['linear'],
              ['get', 'reflectivity'],
              0,
              0.3,
              10,
              0.5,
              20,
              0.7,
              30,
              0.9,
              40,
              1,
            ],
            'heatmap-intensity': 5,
            'heatmap-color': [
              'interpolate',
              ['linear'],
              ['get', 'reflectivity'],
              ...RADAR_COLORS.flat(),
            ],
            'heatmap-radius': 80,
            'heatmap-opacity': 1,
          },
        });

        console.log(`✅ Heatmap layer added with ${data.features.length} points`);
      } catch (error) {
        console.error('Error:', error);
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
