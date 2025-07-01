'use client';

import 'leaflet/dist/leaflet.css';
import { useState, useEffect, memo } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';

import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

// Fix for default marker icon issue with Webpack
delete (L.Icon.Default.prototype as any)._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x.src,
  iconUrl: markerIcon.src,
  shadowUrl: markerShadow.src,
});

interface MarkerData {
  koordinat: { x: number; y: number };
  companies: { id: string; firma_unvani: string | null; adres: string | null }[];
}

interface MapDisplayProps {
  markers: MarkerData[];
}

const MapDisplay = memo(({ markers }: MapDisplayProps) => {
  // Default center for the map (Turkey)
  // Türkiye'yi daha iyi ortalamak için harita merkezi güncellendi.
  const position: [number, number] = [39.0, 35.5];
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  if (!isMounted) {
    return null;
  }

  return (
    <MapContainer center={position} zoom={5} scrollWheelZoom={true} style={{ height: '100%', width: '100%' }}>
      <>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
          url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
        />
        {markers.map((marker, index) => (
          <Marker key={index} position={[marker.koordinat.y, marker.koordinat.x]}>
            <Popup>
              <div className="space-y-2">
                {marker.companies.map(company => (
                  <div key={company.id}>
                    <div className="font-bold">{company.firma_unvani || 'İsim Bilgisi Yok'}</div>
                    <div className="text-sm text-gray-600">{company.adres || 'Adres Bilgisi Yok'}</div>
                  </div>
                ))}
              </div>
            </Popup>
          </Marker>
        ))}
      </>
    </MapContainer>
  );
});

MapDisplay.displayName = 'MapDisplay';

export default MapDisplay;
