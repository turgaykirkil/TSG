'use client';

import 'leaflet/dist/leaflet.css';
import { memo, useState, useMemo, useEffect, useCallback } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap, ZoomControl } from 'react-leaflet';
import L, { LatLngExpression, LatLngBoundsExpression } from 'leaflet';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';
import apiClient from '@/lib/api/client';

export interface CompanyMapPin {
  id: string;
  unvan: string;
  address: string;
  city: string;
  district: string;
  lat: number;
  lon: number;
  precision?: string;
}

interface AdminCoordinatesMapProps {
  pins: CompanyMapPin[];
  onCoordinateUpdated?: () => void;
  height?: string;
}

// Custom Leaflet Icons by Precision / Type
const createCustomIcon = (color: string) => {
  return L.divIcon({
    className: 'custom-leaflet-marker',
    html: `
      <div style="
        background-color: ${color};
        width: 26px;
        height: 26px;
        border-radius: 50%;
        border: 2px solid white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 12px;
        font-weight: bold;
      ">
        📍
      </div>
    `,
    iconSize: [26, 26],
    iconAnchor: [13, 13],
    popupAnchor: [0, -13],
  });
};

const iconGreen = createCustomIcon('#10b981'); // Exact / High precision
const iconBlue = createCustomIcon('#3b82f6');  // Street precision
const iconYellow = createCustomIcon('#f59e0b'); // Neighbourhood / District

// Cluster Icon Generator
const createClusterIcon = (count: number) => {
  let bgColor = '#10b981'; // Green
  let size = 34;

  if (count >= 20) {
    bgColor = '#6366f1'; // Indigo / Large cluster
    size = 42;
  } else if (count >= 6) {
    bgColor = '#3b82f6'; // Blue / Medium cluster
    size = 38;
  }

  return L.divIcon({
    className: 'custom-cluster-icon',
    html: `
      <div style="
        background-color: ${bgColor};
        width: ${size}px;
        height: ${size}px;
        border-radius: 50%;
        border: 3px solid white;
        box-shadow: 0 4px 14px rgba(0,0,0,0.45);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: -0.5px;
      ">
        ${count}
      </div>
    `,
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2],
  });
};

// Sub-component to handle map state, zoom events, and view controls
function MapController({
  viewTarget,
  pins,
  onZoomChange,
}: {
  viewTarget: 'turkey' | 'fit' | null;
  pins: CompanyMapPin[];
  onZoomChange: (zoom: number) => void;
}) {
  const map = useMap();

  useEffect(() => {
    const handleZoom = () => {
      onZoomChange(map.getZoom());
    };
    map.on('zoomend', handleZoom);
    return () => {
      map.off('zoomend', handleZoom);
    };
  }, [map, onZoomChange]);

  useEffect(() => {
    const timer = setTimeout(() => {
      try {
        map.invalidateSize();
      } catch (err) {
        // ignore
      }
    }, 100);
    return () => clearTimeout(timer);
  }, [map]);

  useEffect(() => {
    if (viewTarget === 'turkey') {
      map.setView([39.0, 35.5], 6, { animate: true });
    } else if (viewTarget === 'fit' && pins.length > 0) {
      const bounds: LatLngBoundsExpression = pins.map((p) => [p.lat, p.lon]);
      map.fitBounds(bounds, { padding: [50, 50], maxZoom: 15, animate: true });
    }
  }, [viewTarget, map, pins]);

  return null;
}

function AdminCoordinatesMapBase({ pins = [], onCoordinateUpdated, height = '620px' }: AdminCoordinatesMapProps) {
  const [selectedStyle, setSelectedStyle] = useState<'dark' | 'light' | 'osm' | 'satellite'>('dark');
  const [viewTarget, setViewTarget] = useState<'turkey' | 'fit' | null>('turkey');
  const [updatingPinId, setUpdatingPinId] = useState<string | null>(null);
  const [currentZoom, setCurrentZoom] = useState<number>(6);

  // Turkey Center default view
  const turkeyCenter: LatLngExpression = [39.0, 35.5];

  // Dynamic Clustering Logic
  const { clusters, individualPins } = useMemo(() => {
    if (currentZoom >= 14 || pins.length <= 1) {
      return { clusters: [], individualPins: pins };
    }

    // Grid size in degrees based on zoom level
    const gridSize = 180 / Math.pow(2, currentZoom + 2);
    const grid: Record<string, CompanyMapPin[]> = {};

    pins.forEach((pin) => {
      const latCell = Math.floor(pin.lat / gridSize);
      const lonCell = Math.floor(pin.lon / gridSize);
      const key = `${latCell}_${lonCell}`;
      if (!grid[key]) grid[key] = [];
      grid[key].push(pin);
    });

    const clusterList: { id: string; lat: number; lon: number; count: number; pins: CompanyMapPin[] }[] = [];
    const indList: CompanyMapPin[] = [];

    Object.entries(grid).forEach(([key, items]) => {
      if (items.length > 1) {
        const avgLat = items.reduce((sum, p) => sum + p.lat, 0) / items.length;
        const avgLon = items.reduce((sum, p) => sum + p.lon, 0) / items.length;
        clusterList.push({
          id: `cluster_${key}`,
          lat: avgLat,
          lon: avgLon,
          count: items.length,
          pins: items,
        });
      } else {
        indList.push(items[0]);
      }
    });

    return { clusters: clusterList, individualPins: indList };
  }, [pins, currentZoom]);

  const tileUrls = {
    dark: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
    light: 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
    osm: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    satellite: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
  };

  const handleMarkerDragEnd = useCallback(async (pinId: string, event: any) => {
    const marker = event.target;
    if (!marker) return;
    const latLng = marker.getLatLng();
    const newLat = parseFloat(latLng.lat.toFixed(7));
    const newLon = parseFloat(latLng.lng.toFixed(7));

    setUpdatingPinId(pinId);
    try {
      await apiClient.post(`/api/v1/companies/${pinId}/update-coordinate/`, {
        lat: newLat,
        lon: newLon,
      });
      toast.success(`Şirket konumu haritada güncellendi: ${newLat}, ${newLon}`);
      if (onCoordinateUpdated) onCoordinateUpdated();
    } catch (err: any) {
      toast.error('Konum güncellenirken hata oluştu.');
    } finally {
      setUpdatingPinId(null);
    }
  }, [onCoordinateUpdated]);

  return (
    <div className="relative w-full rounded-xl border bg-card text-card-foreground shadow-lg overflow-hidden" style={{ height }}>
      {/* Floating Controls Bar */}
      <div className="absolute top-3 left-3 z-[400] flex flex-wrap items-center gap-2 bg-background/95 border border-border p-1.5 rounded-lg shadow-md max-w-[calc(100%-60px)]">
        {/* Style Selector */}
        <div className="flex items-center gap-1 bg-muted/50 p-0.5 rounded-md">
          <Button
            variant={selectedStyle === 'dark' ? 'default' : 'ghost'}
            size="sm"
            onClick={() => setSelectedStyle('dark')}
            className="text-xs h-7 px-2"
          >
            🌙 Koyu
          </Button>
          <Button
            variant={selectedStyle === 'light' ? 'default' : 'ghost'}
            size="sm"
            onClick={() => setSelectedStyle('light')}
            className="text-xs h-7 px-2"
          >
            ☀️ Açık
          </Button>
          <Button
            variant={selectedStyle === 'osm' ? 'default' : 'ghost'}
            size="sm"
            onClick={() => setSelectedStyle('osm')}
            className="text-xs h-7 px-2"
          >
            🗺️ Klasik
          </Button>
          <Button
            variant={selectedStyle === 'satellite' ? 'default' : 'ghost'}
            size="sm"
            onClick={() => setSelectedStyle('satellite')}
            className="text-xs h-7 px-2"
          >
            🛰️ Uydu
          </Button>
        </div>

        <div className="h-4 w-px bg-border hidden sm:block" />

        {/* Zoom / Bounds Controls */}
        <div className="flex items-center gap-1">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setViewTarget('turkey')}
            className="text-xs h-7 px-2 gap-1"
          >
            🇹🇷 Tüm Türkiye
          </Button>
          {pins.length > 0 && (
            <Button
              variant="outline"
              size="sm"
              onClick={() => setViewTarget('fit')}
              className="text-xs h-7 px-2 gap-1"
            >
              🎯 Şirketlere Odaklan
            </Button>
          )}
        </div>

        <div className="h-4 w-px bg-border hidden sm:block" />

        <span className="text-xs text-muted-foreground font-semibold px-1">
          {pins.length} Şirket Haritada
        </span>
      </div>

      <MapContainer
        center={turkeyCenter}
        zoom={6}
        scrollWheelZoom={true}
        zoomControl={false}
        style={{ width: '100%', height: '100%' }}
        className="z-0 w-full h-full block"
      >
        <MapController viewTarget={viewTarget} pins={pins} onZoomChange={setCurrentZoom} />
        <TileLayer
          url={tileUrls[selectedStyle]}
          subdomains={['a', 'b', 'c', 'd']}
          attribution='&copy; OpenStreetMap, CartoDB & Esri'
        />
        <ZoomControl position="topright" />

        {/* Render Cluster Badge Markers for Overlapping Companies */}
        {clusters.map((cluster) => (
          <Marker
            key={cluster.id}
            position={[cluster.lat, cluster.lon]}
            icon={createClusterIcon(cluster.count)}
          >
            <Popup className="rounded-lg shadow-lg">
              <div className="p-1 space-y-2 max-w-[280px]">
                <div className="flex items-center justify-between border-b pb-1">
                  <h4 className="font-bold text-sm text-foreground">
                    📍 {cluster.count} Şirket Konumlandı
                  </h4>
                </div>
                <div className="max-h-[140px] overflow-y-auto space-y-1 text-xs text-muted-foreground pr-1">
                  {cluster.pins.map((p, idx) => (
                    <div key={p.id} className="border-b border-border/40 pb-1 pt-0.5">
                      <p className="font-semibold text-foreground truncate">{idx + 1}. {p.unvan}</p>
                      <p className="text-[11px] truncate opacity-80">{p.address}</p>
                    </div>
                  ))}
                </div>
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Render Individual Markers */}
        {individualPins.map((pin) => {
          const icon = pin.precision === 'EXACT_BUILDING' ? iconGreen : pin.precision === 'STREET_LEVEL' ? iconBlue : iconYellow;
          return (
            <Marker
              key={pin.id}
              position={[pin.lat, pin.lon]}
              icon={icon}
              draggable={true}
              eventHandlers={{
                dragend: (e) => handleMarkerDragEnd(pin.id, e),
              }}
            >
              <Popup className="rounded-lg shadow-lg">
                <div className="p-1 space-y-1.5 max-w-[280px]">
                  <div className="flex items-center justify-between border-b pb-1">
                    <h4 className="font-bold text-sm text-foreground truncate">{pin.unvan}</h4>
                  </div>
                  <p className="text-xs text-muted-foreground leading-relaxed">{pin.address}</p>
                  
                  <div className="flex items-center justify-between pt-1 text-[11px] text-slate-500 border-t">
                    <span>📍 {pin.lat.toFixed(5)}, {pin.lon.toFixed(5)}</span>
                    <span className="font-semibold text-emerald-600 dark:text-emerald-400">
                      Sürükleyerek Düzenle 🖐️
                    </span>
                  </div>
                  {updatingPinId === pin.id && (
                    <p className="text-xs text-amber-500 font-semibold animate-pulse">Kaydediliyor...</p>
                  )}
                </div>
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>
    </div>
  );
}

export const AdminCoordinatesMap = memo(AdminCoordinatesMapBase);
