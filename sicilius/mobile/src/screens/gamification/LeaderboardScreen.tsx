import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  TouchableOpacity,
  FlatList,
  Dimensions
} from 'react-native';
import { MaterialCommunityIcons as Icon } from '@expo/vector-icons';
import { useGamificationStore } from '../../store/gamificationStore';
import { lightColors } from '../../theme';
import { LeaderboardRankItem, DailyQuestItem } from '../../types/gamification';

const { width: screenWidth } = Dimensions.get('window');

// Rozet Kataloğu Tanımı
const BADGES_LIST = [
  { code: 'STREET_HUNTER', title: 'Sokak Avcısı', icon: 'car-sports', color: '#0EA5E9', desc: '50 Müşteri Ziyareti', unlocked: true },
  { code: 'COMPASS_MASTER', title: 'Pusula Ustası', icon: 'compass-outline', color: '#10B981', desc: '20 Konum Doğrulama', unlocked: true },
  { code: 'DATA_SECURITY', title: 'Veri Güvenliği', icon: 'shield-check-outline', color: '#6366F1', desc: 'KVKK Uyumlu Kayıt', unlocked: true },
  { code: 'LIGHTNING_ROUTE', title: 'Şimşek Rota', icon: 'flash-outline', color: '#F59E0B', desc: 'Zamanında Rota', unlocked: false },
  { code: 'FIELD_TIGER', title: 'Saha Kaplanı', icon: 'fire', color: '#EF4444', desc: '7 Günlük Ziyaret Serisi', unlocked: false },
  { code: 'MAP_ARCHITECT', title: 'Harita Mimarı', icon: 'map-marker-path', color: '#8B5CF6', desc: '50m Hassas Yerleşimi', unlocked: false },
];

// Fallback Hedefler (Günlük & Haftalık)
const DAILY_TARGETS: DailyQuestItem[] = [
  { id: 'd1', title: '5 km Yarıçapında 3 Ziyaret Yap', quest_type: 'distance', target_count: 3, current_progress: 2, xp_reward: 80, is_completed: false },
  { id: 'd2', title: 'Haritada 2 Firmanın Konumunu Doğrula', quest_type: 'coord_correction', target_count: 2, current_progress: 1, xp_reward: 100, is_completed: false },
  { id: 'd3', title: 'OCR İle Metin Bilgilerini Eksiksiz Kaydet', quest_type: 'ocr_data', target_count: 1, current_progress: 1, xp_reward: 50, is_completed: true },
];

const WEEKLY_TARGETS: DailyQuestItem[] = [
  { id: 'w1', title: '5 Gün Kesintisiz Ziyaret Serisi Yakala', quest_type: 'streak', target_count: 5, current_progress: 3, xp_reward: 250, is_completed: false },
  { id: 'w2', title: 'Haftada 15 Müşteri Ziyaretini Tamamla', quest_type: 'distance', target_count: 15, current_progress: 8, xp_reward: 300, is_completed: false },
  { id: 'w3', title: '10 Hatalı Harita Pinini Yerinde Güncelle', quest_type: 'coord_correction', target_count: 10, current_progress: 4, xp_reward: 200, is_completed: false },
];

// Fallback Sıralama Verisi (KVKK Uyumlu İsimsiz)
const DEMO_LEADERBOARD: LeaderboardRankItem[] = [
  { rank: 1, anonymous_label: 'Temsilci #104', xp: 7450, is_current_user: false },
  { rank: 2, anonymous_label: 'Temsilci #88', xp: 6900, is_current_user: false },
  { rank: 3, anonymous_label: 'Temsilci #12', xp: 6200, is_current_user: false },
  { rank: 4, anonymous_label: 'SEN (4. Sıra)', xp: 5850, is_current_user: true },
  { rank: 5, anonymous_label: 'Temsilci #53', xp: 5100, is_current_user: false },
  { rank: 6, anonymous_label: 'Temsilci #29', xp: 4750, is_current_user: false },
  { rank: 7, anonymous_label: 'Temsilci #91', xp: 4200, is_current_user: false },
];

const LeaderboardScreen: React.FC = () => {
  const { profile, leaderboard, fetchProfile, fetchLeaderboard } = useGamificationStore();
  const [targetTab, setTargetTab] = useState<'daily' | 'weekly'>('daily');

  useEffect(() => {
    fetchProfile();
    fetchLeaderboard();
  }, []);

  const activeTargets = targetTab === 'daily' ? DAILY_TARGETS : WEEKLY_TARGETS;
  const currentRankings = (leaderboard?.rankings && leaderboard.rankings.length > 0)
    ? leaderboard.rankings
    : DEMO_LEADERBOARD;

  const userXP = profile?.xp_points || 5850;
  const streakDays = profile?.streak_days || 3;
  const currentLeague = profile?.current_league || 'Altın Ligi';

  const renderRankItem = ({ item }: { item: LeaderboardRankItem }) => (
    <View style={[
      styles.rankCard,
      item.is_current_user && styles.currentUserRankCard
    ]}>
      <View style={[
        styles.rankBadge,
        item.rank === 1 && { backgroundColor: '#F59E0B' },
        item.rank === 2 && { backgroundColor: '#94A3B8' },
        item.rank === 3 && { backgroundColor: '#D97706' },
        item.rank > 3 && { backgroundColor: lightColors.border }
      ]}>
        <Text style={[
          styles.rankBadgeText,
          item.rank > 3 && { color: lightColors.text }
        ]}>{item.rank}</Text>
      </View>

      <View style={{ flex: 1 }}>
        <Text style={[
          styles.rankLabel,
          item.is_current_user && styles.currentUserRankLabel
        ]}>
          {item.anonymous_label}
        </Text>
        <Text style={styles.rankSubText}>
          {item.is_current_user ? 'Saha Liginde Top %10 Dilimdesin' : 'Saha Temsilcisi'}
        </Text>
      </View>

      <View style={[
        styles.xpBox,
        item.is_current_user && { backgroundColor: '#0EA5E9' }
      ]}>
        <Text style={[
          styles.xpText,
          item.is_current_user && { color: '#FFFFFF' }
        ]}>{item.xp} XP</Text>
      </View>
    </View>
  );

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView style={styles.container} showsVerticalScrollIndicator={false} contentContainerStyle={{ paddingBottom: 40 }}>
        
        {/* ─── Top Brand Banner (Sicilius Cyan & Indigo Theme) ─── */}
        <View style={styles.headerBanner}>
          <View style={styles.headerRow}>
            <View style={{ flex: 1 }}>
              <View style={styles.leagueChip}>
                <Icon name="shield-crown-outline" size={16} color="#0EA5E9" />
                <Text style={styles.leagueChipText}>{currentLeague}</Text>
              </View>
              <Text style={styles.xpTitle}>{userXP.toLocaleString('tr-TR')} XP</Text>
            </View>
            <View style={styles.streakBadge}>
              <Icon name="fire" size={22} color="#EF4444" />
              <Text style={styles.streakText}>{streakDays} Gün Seri</Text>
            </View>
          </View>

          {/* Level Progress */}
          <View style={styles.progressContainer}>
            <View style={styles.progressBarBg}>
              <View style={[
                styles.progressBarFill,
                { width: `${Math.min(100, (userXP % 1000) / 10)}%` }
              ]} />
            </View>
            <View style={styles.progressTextRow}>
              <Text style={styles.progressText}>Seviye {Math.floor(userXP / 1000) + 1}</Text>
              <Text style={styles.progressText}>Sonraki Seviyeye {1000 - (userXP % 1000)} XP</Text>
            </View>
          </View>
        </View>

        {/* ─── Daily & Weekly Targets Section (Segmented Switcher) ─── */}
        <View style={styles.sectionHeader}>
          <Icon name="target" size={22} color={lightColors.primary} />
          <Text style={styles.sectionTitle}>Saha Hedefleri & Görevler</Text>
        </View>

        {/* Tab Switcher */}
        <View style={styles.tabContainer}>
          <TouchableOpacity
            style={[styles.tabButton, targetTab === 'daily' && styles.tabButtonActive]}
            activeOpacity={0.8}
            onPress={() => setTargetTab('daily')}>
            <Icon name="calendar-today" size={16} color={targetTab === 'daily' ? '#FFFFFF' : lightColors.subtext} />
            <Text style={[styles.tabText, targetTab === 'daily' && styles.tabTextActive]}>
              Günlük Hedefler
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.tabButton, targetTab === 'weekly' && styles.tabButtonActive]}
            activeOpacity={0.8}
            onPress={() => setTargetTab('weekly')}>
            <Icon name="calendar-week" size={16} color={targetTab === 'weekly' ? '#FFFFFF' : lightColors.subtext} />
            <Text style={[styles.tabText, targetTab === 'weekly' && styles.tabTextActive]}>
              Haftalık Hedefler
            </Text>
          </TouchableOpacity>
        </View>

        {/* Targets List */}
        {activeTargets.map((item) => (
          <View key={item.id} style={styles.targetCard}>
            <View style={styles.targetHeader}>
              <View style={{ flex: 1, paddingRight: 8 }}>
                <Text style={styles.targetTitle}>{item.title}</Text>
                <Text style={styles.targetCategory}>
                  {item.quest_type === 'distance' ? '📍 GPS Ziyareti' : item.quest_type === 'coord_correction' ? '🛰️ Konum Doğrulama' : '📋 OCR Veri Aktarımı'}
                </Text>
              </View>
              <View style={[
                styles.xpRewardBadge,
                item.is_completed && { backgroundColor: '#D1FAE5' }
              ]}>
                <Text style={[
                  styles.xpRewardText,
                  item.is_completed && { color: '#059669' }
                ]}>
                  {item.is_completed ? 'Tamamlandı ✓' : `+${item.xp_reward} XP`}
                </Text>
              </View>
            </View>

            <View style={styles.targetProgressRow}>
              <View style={styles.targetProgressBg}>
                <View style={[
                  styles.targetProgressFill,
                  { width: `${(item.current_progress / item.target_count) * 100}%` },
                  item.is_completed && { backgroundColor: '#10B981' }
                ]} />
              </View>
              <Text style={styles.targetProgressText}>
                {item.current_progress} / {item.target_count}
              </Text>
            </View>
          </View>
        ))}

        {/* ─── Rozet Vitrini (Badges Showcase) ─── */}
        <View style={styles.sectionHeader}>
          <Icon name="medal-outline" size={22} color={lightColors.primary} />
          <Text style={styles.sectionTitle}>Rozet Vitrini (Kazanılanlar)</Text>
        </View>

        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.badgesScrollView}>
          {BADGES_LIST.map((badge) => (
            <View key={badge.code} style={[
              styles.badgeCard,
              !badge.unlocked && styles.badgeCardLocked
            ]}>
              <View style={[
                styles.badgeIconCircle,
                { backgroundColor: badge.unlocked ? `${badge.color}15` : '#F1F5F9' }
              ]}>
                <Icon
                  name={badge.icon as any}
                  size={26}
                  color={badge.unlocked ? badge.color : '#94A3B8'}
                />
              </View>
              <Text style={styles.badgeTitle}>{badge.title}</Text>
              <Text style={styles.badgeDesc}>{badge.desc}</Text>
              <View style={[
                styles.badgeStatusPill,
                badge.unlocked ? { backgroundColor: '#E0F2FE' } : { backgroundColor: '#F1F5F9' }
              ]}>
                <Text style={[
                  styles.badgeStatusText,
                  badge.unlocked ? { color: '#0284C7' } : { color: '#94A3B8' }
                ]}>
                  {badge.unlocked ? 'Kazanıldı ✓' : 'Kilitli 🔒'}
                </Text>
              </View>
            </View>
          ))}
        </ScrollView>

        {/* ─── Privacy-First Anonymous Leaderboard ─── */}
        <View style={styles.sectionHeader}>
          <Icon name="trophy-outline" size={22} color={lightColors.primary} />
          <Text style={styles.sectionTitle}>Saha Ligi Sıralaması (Gizlilik Korumalı)</Text>
        </View>

        <FlatList
          data={currentRankings}
          keyExtractor={(item) => String(item.rank)}
          renderItem={renderRankItem}
          scrollEnabled={false}
        />
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#F8FAFC',
  },
  container: {
    flex: 1,
    padding: 16,
  },
  headerBanner: {
    backgroundColor: '#0F172A', // Brand Deep Slate / Cyan Accent
    borderRadius: 20,
    padding: 20,
    marginBottom: 20,
    borderWidth: 1,
    borderColor: '#1E293B',
    elevation: 4,
    shadowColor: '#0EA5E9',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 8,
  },
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  leagueChip: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(14, 165, 233, 0.15)',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
    alignSelf: 'flex-start',
    gap: 6,
  },
  leagueChipText: {
    color: '#38BDF8',
    fontSize: 13,
    fontWeight: '700',
    textTransform: 'uppercase',
  },
  xpTitle: {
    color: '#FFFFFF',
    fontSize: 32,
    fontWeight: '800',
    marginTop: 6,
  },
  streakBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
    gap: 4,
  },
  streakText: {
    fontSize: 13,
    fontWeight: '700',
    color: '#0F172A',
  },
  progressContainer: {
    marginTop: 4,
  },
  progressBarBg: {
    height: 8,
    backgroundColor: 'rgba(255, 255, 255, 0.15)',
    borderRadius: 4,
    overflow: 'hidden',
  },
  progressBarFill: {
    height: '100%',
    backgroundColor: '#0EA5E9', // Brand Cyan
    borderRadius: 4,
  },
  progressTextRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 6,
  },
  progressText: {
    color: '#94A3B8',
    fontSize: 12,
    fontWeight: '500',
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
    marginTop: 12,
    gap: 8,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#0F172A',
  },
  tabContainer: {
    flexDirection: 'row',
    backgroundColor: '#E2E8F0',
    borderRadius: 12,
    padding: 4,
    marginBottom: 14,
  },
  tabButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 8,
    borderRadius: 10,
    gap: 6,
  },
  tabButtonActive: {
    backgroundColor: '#0EA5E9',
  },
  tabText: {
    fontSize: 13,
    fontWeight: '600',
    color: '#64748B',
  },
  tabTextActive: {
    color: '#FFFFFF',
    fontWeight: '700',
  },
  targetCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    padding: 14,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: '#E2E8F0',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 3,
  },
  targetHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 10,
  },
  targetTitle: {
    fontSize: 14,
    fontWeight: '700',
    color: '#0F172A',
  },
  targetCategory: {
    fontSize: 12,
    color: '#64748B',
    marginTop: 2,
  },
  xpRewardBadge: {
    backgroundColor: '#FEF3C7',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  xpRewardText: {
    color: '#D97706',
    fontWeight: '700',
    fontSize: 12,
  },
  targetProgressRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  targetProgressBg: {
    flex: 1,
    height: 8,
    backgroundColor: '#F1F5F9',
    borderRadius: 4,
    overflow: 'hidden',
    marginRight: 10,
  },
  targetProgressFill: {
    height: '100%',
    backgroundColor: '#0EA5E9',
    borderRadius: 4,
  },
  targetProgressText: {
    fontSize: 12,
    color: '#475569',
    fontWeight: '700',
  },
  badgesScrollView: {
    marginBottom: 16,
    marginHorizontal: -16,
    paddingHorizontal: 16,
  },
  badgeCard: {
    width: 125,
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    padding: 12,
    marginRight: 10,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#E2E8F0',
  },
  badgeCardLocked: {
    opacity: 0.6,
  },
  badgeIconCircle: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 8,
  },
  badgeTitle: {
    fontSize: 13,
    fontWeight: '700',
    color: '#0F172A',
    textAlign: 'center',
  },
  badgeDesc: {
    fontSize: 10,
    color: '#64748B',
    textAlign: 'center',
    marginTop: 2,
    height: 26,
  },
  badgeStatusPill: {
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 10,
    marginTop: 6,
  },
  badgeStatusText: {
    fontSize: 10,
    fontWeight: '700',
  },
  rankCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    padding: 12,
    marginBottom: 8,
    borderWidth: 1,
    borderColor: '#E2E8F0',
  },
  currentUserRankCard: {
    backgroundColor: '#F0F9FF',
    borderColor: '#0EA5E9',
    borderWidth: 1.5,
  },
  rankBadge: {
    width: 32,
    height: 32,
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  rankBadgeText: {
    color: '#FFFFFF',
    fontWeight: '800',
    fontSize: 14,
  },
  rankLabel: {
    fontSize: 14,
    fontWeight: '700',
    color: '#0F172A',
  },
  currentUserRankLabel: {
    color: '#0284C7',
    fontWeight: '800',
  },
  rankSubText: {
    fontSize: 11,
    color: '#64748B',
    marginTop: 1,
  },
  xpBox: {
    backgroundColor: '#F1F5F9',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
  },
  xpText: {
    fontSize: 13,
    fontWeight: '700',
    color: '#0F172A',
  },
});

export default LeaderboardScreen;
