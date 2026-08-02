import axios from 'axios';

const OPENWEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather';
const WEATHER_API_KEY = process.env.EXPO_PUBLIC_OPENWEATHER_API_KEY || process.env.OPENWEATHER_API_KEY || 'ae30c9da2647cfe9a92252ddb9b42873';

export class WeatherService {
  private static instance: WeatherService;
  private api = axios.create({ baseURL: OPENWEATHER_API_URL });

  private constructor() {}

  public static getInstance(): WeatherService {
    if (!WeatherService.instance) {
      WeatherService.instance = new WeatherService();
    }
    return WeatherService.instance;
  }

  async getCurrentWeather(lat: number, lon: number) {
    try {
      const response = await this.api.get('', {
        params: {
          lat,
          lon,
          appid: WEATHER_API_KEY,
          units: 'metric'
        }
      });

      return {
        temperature: response.data.main.temp,
        feelsLike: response.data.main.feels_like,
        condition: response.data.weather[0].main,
        description: response.data.weather[0].description,
        windSpeed: response.data.wind.speed,
        humidity: response.data.main.humidity
      };
    } catch (error) {
      console.error('Hava durumu alınamadı:', error);
      throw error;
    }
  }

  async getForecast(lat: number, lon: number, days: number = 5) {
    try {
      const response = await axios.get('https://api.openweathermap.org/data/2.5/forecast', {
        params: {
          lat,
          lon,
          appid: WEATHER_API_KEY,
          units: 'metric',
          cnt: days * 8 // Her gün için 8 veri noktası
        }
      });

      return response.data.list.map(forecast => ({
        date: forecast.dt_txt,
        temperature: forecast.main.temp,
        condition: forecast.weather[0].main,
        windSpeed: forecast.wind.speed
      }));
    } catch (error) {
      console.error('Hava durumu tahmini alınamadı:', error);
      throw error;
    }
  }
}
