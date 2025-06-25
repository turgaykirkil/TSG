'use client';

import 'leaflet/dist/leaflet.css';
import { useState, useEffect } from 'react';
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
  companies: { id: string; firma_unvani: string; adres: string }[];
}

interface MapDisplayProps {
  markers: MarkerData[];
}

const MapDisplay = ({ markers }: MapDisplayProps) => {
  // Default center for the map (Turkey)
  const position: [number, number] = [39.9334, 32.8597];
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  if (!isMounted) {
    return null;
  }

  return (
    <MapContainer center={position} zoom={6} scrollWheelZoom={true} style={{ height: '100%', width: '100%' }}>
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
                    <div className="font-bold">{company.firma_unvani}</div>
                    <div className="text-sm text-gray-600">{company.adres}</div>
                  </div>
                ))}
              </div>
            </Popup>
          </Marker>
        ))}
      </>
    </MapContainer>
  );
};

export default MapDisplay;
