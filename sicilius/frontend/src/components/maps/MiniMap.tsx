"use client";

import 'leaflet/dist/leaflet.css';

import { MapContainer, TileLayer, CircleMarker, Tooltip, useMap, ZoomControl } from 'react-leaflet';
import type { LatLngExpression } from 'leaflet';
import { memo, useMemo, useState, useEffect } from 'react';

export interface MiniMapPin {
  id: string;
  lat: number;
  lon: number;
  label?: string | null;
  distance_km?: number;
}

interface MiniMapProps {
  center: { lat: number; lon: number };
  pins?: MiniMapPin[];
  height?: number;
  zoom?: number;
}

function MiniMapBase({ center, pins = [], height = 220, zoom = 13 }: MiniMapProps) {
  const mapCenter = useMemo<LatLngExpression>(() => [center.lat, center.lon], [center.lat, center.lon]);
  const displayPins = Array.isArray(pins) ? pins.slice(0, 30) : [];
  // Use server-side proxy by default to avoid exposing tokens
  const envTileUrl = process.env.NEXT_PUBLIC_MAP_TILE_URL || '/api/map/tiles/{z}/{x}/{y}.png';
  const defaultAttribution = 'Map data © OpenStreetMap contributors, Imagery © LocationIQ';
  const envAttribution = process.env.NEXT_PUBLIC_MAP_ATTRIBUTION || defaultAttribution;
  const [tileUrl, setTileUrl] = useState(envTileUrl);
  const [attribution, setAttribution] = useState(envAttribution);
  const subdomainsRaw = process.env.NEXT_PUBLIC_MAP_TILE_SUBDOMAINS || '';
  const subdomains = useMemo(() => {
    if (!subdomainsRaw) return null as unknown as string | string[] | null;
    // Allow formats like "abc" or "a,b,c" or "1,2,3,4"
    if (subdomainsRaw.includes(',')) return subdomainsRaw.split(',').map(s => s.trim()).filter(Boolean);
    return subdomainsRaw;
  }, [subdomainsRaw]);

  return (
    <div className="rounded border bg-white dark:bg-slate-900 dark:border-slate-700 overflow-hidden w-full min-w-0" style={{ height }}>
      <MapContainer
        key={`${center.lat},${center.lon},${height},${zoom},${tileUrl}`}
        center={mapCenter}
        zoom={zoom}
        scrollWheelZoom={false}
        zoomControl={false}
        style={{ width: '100%', height: '100%' }}
        className="z-0 w-full h-full block"
      >
        {/** Ensure Leaflet recalculates size when inside dialogs/modals */}
        {(() => {
          function MapSizeFixer() {
            const map = useMap();
            useEffect(() => {
              const id = setTimeout(() => {
                try { map.invalidateSize(); } catch {}
              }, 75);
              return () => clearTimeout(id);
            }, [map]);
            useEffect(() => {
              const container = map.getContainer();
              const ro = new ResizeObserver(() => {
                try { map.invalidateSize(); } catch {}
              });
              ro.observe(container);
              return () => {
                try { ro.disconnect(); } catch {}
              };
            }, [map]);
            return null;
          }
          return <MapSizeFixer />;
        })()}
        {(() => {
          const props: any = { attribution, url: tileUrl };
          if (tileUrl.includes('{s}') && subdomains) {
            props.subdomains = subdomains as any;
          }
          props.eventHandlers = {
            tileerror: () => {
              // Fallback to local OSM proxy to avoid COEP/CSP cross-origin restrictions
              const fallbackUrl = '/api/map/osm/tiles/{z}/{x}/{y}.png';
              if (tileUrl !== fallbackUrl) {
                // eslint-disable-next-line no-console
                console.warn('[MiniMap] Tile load failed; falling back to local OSM proxy tiles.');
                setTileUrl(fallbackUrl);
                setAttribution('&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors');
              }
            },
          };
          return <TileLayer key={tileUrl} {...props} />;
        })()}
        {/* Zoom controls (top-right) */}
        <ZoomControl position="topright" />
        {/* Center marker */}
        <CircleMarker center={mapCenter} radius={8} pathOptions={{ color: '#2563eb', fillColor: '#2563eb', fillOpacity: 0.9 }}>
          <Tooltip direction="top" offset={[0, -8]} opacity={1} permanent>
            Merkez
          </Tooltip>
        </CircleMarker>
        {/* Nearby pins */}
        {displayPins.map((p) => (
          <CircleMarker
            key={p.id}
            center={[p.lat, p.lon] as LatLngExpression}
            radius={6}
            pathOptions={{ color: '#059669', fillColor: '#059669', fillOpacity: 0.85 }}
          >
            <Tooltip direction="top" offset={[0, -6]} opacity={1} permanent>
              <div className="text-xs">
                {p.label || 'Yakın şirket'}
                {typeof p.distance_km === 'number' ? ` • ${p.distance_km.toFixed(2)} km` : ''}
              </div>
            </Tooltip>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
}

export const MiniMap = memo(MiniMapBase);
