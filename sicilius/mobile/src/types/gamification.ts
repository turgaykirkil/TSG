export interface CheckInPayload {
  customer_id: string;
  latitude: number;
  longitude: number;
  note_text?: string;
  ocr_data_json?: Record<string, any>;
}

export interface CheckInResult {
  success: boolean;
  message: string;
  xp_gained: number;
  total_xp: number;
  streak_days: number;
  streak_multiplier: number;
  distance_meters: number;
  badges_unlocked: string[];
}

export interface CoordinateCorrectionPayload {
  company_id: string;
  verified_lat: number;
  verified_lon: number;
}

export interface LeaderboardRankItem {
  rank: number;
  anonymous_label: string;
  xp: number;
  is_current_user: boolean;
}

export interface PrivacyLeaderboardData {
  my_rank: number;
  my_xp: number;
  my_league: string;
  percentile_text: string;
  rankings: LeaderboardRankItem[];
}

export interface BadgeItem {
  code: string;
  title: string;
  description: string;
  icon: string;
  category: string;
  is_unlocked: boolean;
  unlocked_at?: string;
}

export interface DailyQuestItem {
  id: string;
  title: string;
  quest_type: string;
  target_count: number;
  current_progress: number;
  xp_reward: number;
  is_completed: boolean;
}

export interface UserGamificationProfile {
  xp_points: number;
  current_level: number;
  current_league: string;
  streak_days: number;
  next_level_xp: number;
  badges_count: number;
  quests_completed_today: number;
}
