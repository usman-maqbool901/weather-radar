import mapboxgl from 'mapbox-gl';
import { MAP_CONFIG } from '../utils/constants';

export const initMapbox = (container: HTMLDivElement, token: string): mapboxgl.Map => {
  mapboxgl.accessToken = token;

  const map = new mapboxgl.Map({
    container,
    style: MAP_CONFIG.style,
    center: MAP_CONFIG.defaultCenter,
    zoom: MAP_CONFIG.defaultZoom,
    minZoom: MAP_CONFIG.minZoom,
    maxZoom: MAP_CONFIG.maxZoom,
    attributionControl: false,
  });

  map.addControl(new mapboxgl.NavigationControl(), 'top-right');
  map.addControl(new mapboxgl.FullscreenControl(), 'top-right');

  return map;
};
