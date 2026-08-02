import axios from 'axios';

const TOMTOM_API_KEY = process.env.EXPO_PUBLIC_TOMTOM_API_KEY || process.env.TOMTOM_API_KEY || '';

export interface TrafficCondition {
  congestionLevel: 'Low' | 'Medium' | 'High';
  averageSpeed: number; // km/h
  delayFactor: number; // multiplier e.g. 1.25 (+25% time)
  description: string;
}

export class TrafficService {
  private static instance: TrafficService;

  private constructor() {}

  public static getInstance(): TrafficService {
    if (!TrafficService.instance) {
      TrafficService.instance = new TrafficService();
    }
    return TrafficService.instance;
  }

  /**
   * Gelismiş Gerçekçi Trafik Koşulu ve Gecikme Çarpanı Hesaplama
   * TomTom API key varsa canlı trafik çeker, yoksa Saat/Mesai + Şehir Trafik Yoğunluğu algoritması kullanır.
   */
  async getTrafficConditions(lat: number, lon: number): Promise<TrafficCondition> {
    if (TOMTOM_API_KEY) {
      try {
        const response = await axios.get(
          `https://api.tomtom.com/traffic/services/4/flowSegmentData/relative0/10/json`,
          {
            params: {
              point: `${lat},${lon}`,
              key: TOMTOM_API_KEY
            },
            timeout: 5000
          }
        );

        const flow = response.data?.flowSegmentData;
        if (flow) {
          const currentSpeed = flow.currentSpeed || 50;
          const freeFlowSpeed = flow.freeFlowSpeed || 50;
          const speedRatio = currentSpeed / Math.max(freeFlowSpeed, 1);

          let congestionLevel: 'Low' | 'Medium' | 'High' = 'Low';
          let delayFactor = 1.0;
          let description = 'Trafik Akıcı';

          if (speedRatio < 0.5) {
            congestionLevel = 'High';
            delayFactor = 1.5;
            description = 'Yoğun Trafik (Gecikme Var)';
          } else if (speedRatio < 0.8) {
            congestionLevel = 'Medium';
            delayFactor = 1.25;
            description = 'Orta Yoğunlukta Trafik';
          }

          return {
            congestionLevel,
            averageSpeed: currentSpeed,
            delayFactor,
            description
          };
        }
      } catch (error) {
        console.log('TomTom canlı trafik çekilemedi, akıllı tahmin algoritması kullanılıyor:', error);
      }
    }

    return this.calculateSmartRushHourTraffic();
  }

  /**
   * Saat ve Şehir İçi Yoğunluk Bazlı Trafik Tahmini
   */
  public calculateSmartRushHourTraffic(): TrafficCondition {
    const now = new Date();
    const hours = now.getHours();
    const minutes = now.getMinutes();
    const timeDecimal = hours + minutes / 60;
    const isWeekend = now.getDay() === 0 || now.getDay() === 6;

    let congestionLevel: 'Low' | 'Medium' | 'High' = 'Low';
    let delayFactor = 1.1; // Şehir içi standart %10 yavaşlama
    let averageSpeed = 50;
    let description = 'Trafik Akıcı';

    if (!isWeekend) {
      if (timeDecimal >= 7.5 && timeDecimal <= 9.5) {
        congestionLevel = 'High';
        delayFactor = 1.4; // %40 ekstra sürüş süresi
        averageSpeed = 28;
        description = 'Sabah Rush Hour (Yoğun Trafik)';
      } else if (timeDecimal >= 17.0 && timeDecimal <= 19.5) {
        congestionLevel = 'High';
        delayFactor = 1.45; // %45 ekstra sürüş süresi
        averageSpeed = 25;
        description = 'Akşam Mesai Çıkışı (Çok Yoğun Trafik)';
      } else if (timeDecimal >= 10.0 && timeDecimal <= 16.5) {
        congestionLevel = 'Medium';
        delayFactor = 1.2; // %20 ekstra sürüş süresi
        averageSpeed = 40;
        description = 'Normal Şehir İçi Trafik';
      }
    } else {
      if (timeDecimal >= 13.0 && timeDecimal <= 18.0) {
        congestionLevel = 'Medium';
        delayFactor = 1.25;
        averageSpeed = 38;
        description = 'Hafta Sonu Trafiği';
      }
    }

    return {
      congestionLevel,
      averageSpeed,
      delayFactor,
      description
    };
  }

  /**
   * Rota için toplam gerçekçi sürüş süresini dakikaya çevirir (Hava durumu + Trafik gecikmesi dahil)
   */
  calculateAdjustedDurationMinutes(
    baseDurationMinutes: number,
    trafficCondition: TrafficCondition,
    weatherCondition?: string
  ): number {
    let multiplier = trafficCondition.delayFactor;

    if (weatherCondition) {
      const cond = weatherCondition.toLowerCase();
      if (cond.includes('rain') || cond.includes('thunderstorm') || cond.includes('drizzle')) {
        multiplier += 0.15; // Yağmurda +%15 ilave gecikme
      } else if (cond.includes('snow') || cond.includes('ice') || cond.includes('sleet')) {
        multiplier += 0.35; // Kar/Buzlanmada +%35 ilave gecikme
      } else if (cond.includes('fog') || cond.includes('mist')) {
        multiplier += 0.10; // Siste +%10 ilave gecikme
      }
    }

    return Math.round(baseDurationMinutes * multiplier);
  }
}
