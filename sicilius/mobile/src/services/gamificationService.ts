import api from './api';
import {
  CheckInPayload,
  CheckInResult,
  CoordinateCorrectionPayload,
  PrivacyLeaderboardData,
  UserGamificationProfile,
  DailyQuestItem
} from '../types/gamification';

export const gamificationService = {
  checkIn: async (payload: CheckInPayload): Promise<CheckInResult> => {
    const response = await api.post('/gamification/check-in', payload);
    return response.data;
  },

  correctCoordinate: async (payload: CoordinateCorrectionPayload) => {
    const response = await api.post('/gamification/self-correct-coordinate', payload);
    return response.data;
  },

  getLeaderboard: async (): Promise<PrivacyLeaderboardData> => {
    const response = await api.get('/gamification/leaderboard');
    return response.data;
  },

  getProfile: async (): Promise<UserGamificationProfile> => {
    const response = await api.get('/gamification/profile');
    return response.data;
  },

  getDailyQuests: async (): Promise<DailyQuestItem[]> => {
    const response = await api.get('/gamification/daily-quests');
    return response.data;
  }
};
