import { create } from 'zustand';
import { gamificationService } from '../services/gamificationService';
import {
  PrivacyLeaderboardData,
  UserGamificationProfile,
  DailyQuestItem,
  CheckInPayload,
  CheckInResult
} from '../types/gamification';

interface GamificationState {
  profile: UserGamificationProfile | null;
  leaderboard: PrivacyLeaderboardData | null;
  dailyQuests: DailyQuestItem[];
  loading: boolean;
  error: string | null;

  fetchProfile: () => Promise<void>;
  fetchLeaderboard: () => Promise<void>;
  fetchDailyQuests: () => Promise<void>;
  performCheckIn: (payload: CheckInPayload) => Promise<CheckInResult>;
  correctCoordinate: (companyId: string, lat: number, lon: number) => Promise<void>;
}

export const useGamificationStore = create<GamificationState>((set, get) => ({
  profile: null,
  leaderboard: null,
  dailyQuests: [],
  loading: false,
  error: null,

  fetchProfile: async () => {
    try {
      set({ loading: true });
      const data = await gamificationService.getProfile();
      set({ profile: data, loading: false });
    } catch (err: any) {
      set({ error: err.message || 'Profil yüklenemedi', loading: false });
    }
  },

  fetchLeaderboard: async () => {
    try {
      set({ loading: true });
      const data = await gamificationService.getLeaderboard();
      set({ leaderboard: data, loading: false });
    } catch (err: any) {
      set({ error: err.message || 'Liderlik tablosu yüklenemedi', loading: false });
    }
  },

  fetchDailyQuests: async () => {
    try {
      const data = await gamificationService.getDailyQuests();
      set({ dailyQuests: data });
    } catch (err: any) {
      console.warn('Quests error:', err);
    }
  },

  performCheckIn: async (payload: CheckInPayload) => {
    const result = await gamificationService.checkIn(payload);
    if (result.success) {
      get().fetchProfile();
      get().fetchLeaderboard();
    }
    return result;
  },

  correctCoordinate: async (companyId: string, lat: number, lon: number) => {
    await gamificationService.correctCoordinate({
      company_id: companyId,
      verified_lat: lat,
      verified_lon: lon
    });
    get().fetchProfile();
  }
}));
