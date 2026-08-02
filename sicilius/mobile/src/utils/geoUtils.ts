// Haversine formülü ile iki koordinat arası mesafeyi hesapla
export function calculateDistance(
  lat1: number, 
  lon1: number, 
  lat2: number, 
  lon2: number
): number {
  const R = 6371; // Dünya yarıçapı (km)
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
    Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c; // Kilometre cinsinden mesafe
}

// Kullanıcının mevcut konumuna göre müşterileri sırala
export function sortCustomersByDistance(
  customers: any[], 
  userLat: number, 
  userLon: number
): any[] {
  return customers.map(customer => ({
    ...customer,
    distance: customer.address?.coordinates 
      ? calculateDistance(
          userLat, 
          userLon, 
          customer.address.coordinates.lat, 
          customer.address.coordinates.lng
        )
      : Infinity
  })).sort((a, b) => a.distance - b.distance);
}
