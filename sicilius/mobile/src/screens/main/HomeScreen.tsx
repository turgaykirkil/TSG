import React, {useCallback, useState, useEffect, useMemo} from 'react';
import {
  View,
  Text,
  Image,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  RefreshControl,
  Dimensions,
  Platform,
} from 'react-native';
import {SafeAreaView} from 'react-native-safe-area-context';
import {useSelector} from 'react-redux';
import {MaterialCommunityIcons as Icon} from '@expo/vector-icons';
import {RootState} from '../../store';
import theme, {lightColors, spacing, typography, shadows} from '../../theme';
import {useNavigation} from '@react-navigation/native';
import {MainTabParamList} from '../../navigation/types';
import {BottomTabNavigationProp} from '@react-navigation/bottom-tabs';
import {customerAPI, taskAPI, salesAPI} from '../../services/api';

const screenWidth = Dimensions.get('window').width;

// ────────────────────────────────────────────────────────────────────────────
// Custom Card Bileşeni — react-native-paper Card yerine
// ────────────────────────────────────────────────────────────────────────────
const Card: React.FC<{style?: any; children: React.ReactNode}> & {
  Content: React.FC<{style?: any; children: React.ReactNode}>;
} = ({style, children}) => (
  <View
    style={[
      {
        backgroundColor: '#FFFFFF',
        borderRadius: 16,
        ...shadows.small,
      },
      style,
    ]}>
    {children}
  </View>
);
Card.Content = ({style, children}) => (
  <View style={[{padding: 16}, style]}>{children}</View>
);

// ────────────────────────────────────────────────────────────────────────────
// Mini Progress Bar — react-native-paper ProgressBar yerine
// ────────────────────────────────────────────────────────────────────────────
const ProgressBar: React.FC<{
  progress: number;
  color?: string;
  style?: any;
}> = ({progress, color = lightColors.primary, style}) => (
  <View
    style={[
      {
        height: 6,
        borderRadius: 3,
        backgroundColor: lightColors.border,
        overflow: 'hidden',
      },
      style,
    ]}>
    <View
      style={{
        height: '100%',
        width: `${Math.min(progress * 100, 100)}%`,
        backgroundColor: color,
        borderRadius: 3,
      }}
    />
  </View>
);

// ────────────────────────────────────────────────────────────────────────────
// Interfaces
// ────────────────────────────────────────────────────────────────────────────
interface Customer {
  id: string;
  name: string;
  company: string;
  salesRepId: string;
}

interface Task {
  id: string;
  title: string;
  description: string;
  status: string;
  dueDate: string;
  priority: string;
  progress?: number;
}

interface Sale {
  id: string;
  amount: number;
  date: string;
}

// ────────────────────────────────────────────────────────────────────────────
// Premium Stat Card Bileşeni
// ────────────────────────────────────────────────────────────────────────────
interface StatCardProps {
  icon: string;
  value: string | number;
  label: string;
  gradient: [string, string]; // [başlangıç, bitiş] renk
  accentColor: string;
}

const StatCard: React.FC<StatCardProps> = ({
  icon,
  value,
  label,
  gradient,
  accentColor,
}) => (
  <View style={statStyles.card}>
    <View
      style={[statStyles.iconCircle, {backgroundColor: `${accentColor}15`}]}>
      <Icon name={icon as any} size={22} color={accentColor} />
    </View>
    <Text style={[statStyles.value, {color: lightColors.text}]}>{value}</Text>
    <Text style={statStyles.label}>{label}</Text>
    <View style={[statStyles.accentBar, {backgroundColor: accentColor}]} />
  </View>
);

const statStyles = StyleSheet.create({
  card: {
    flex: 1,
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 14,
    marginHorizontal: 5,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 130,
    ...shadows.small,
    overflow: 'hidden',
  },
  iconCircle: {
    width: 42,
    height: 42,
    borderRadius: 21,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 10,
  },
  value: {
    fontSize: 22,
    fontWeight: '700',
    marginBottom: 4,
  },
  label: {
    fontSize: 11,
    fontWeight: '500',
    color: lightColors.subtext,
    textAlign: 'center',
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  accentBar: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    height: 3,
    borderBottomLeftRadius: 16,
    borderBottomRightRadius: 16,
  },
});

// ────────────────────────────────────────────────────────────────────────────
// Basit Mini Chart Bileşeni (react-native-chart-kit yerine)
// ────────────────────────────────────────────────────────────────────────────
const MiniBarChart: React.FC<{
  data: number[];
  labels: string[];
  color?: string;
}> = ({data, labels, color = lightColors.primary}) => {
  const maxVal = Math.max(...data, 1);
  const chartHeight = 140;

  return (
    <View style={miniChartStyles.container}>
      <View style={miniChartStyles.barsRow}>
        {data.map((val, i) => {
          const barHeight = (val / maxVal) * chartHeight;
          return (
            <View key={i} style={miniChartStyles.barWrapper}>
              <View
                style={[
                  miniChartStyles.bar,
                  {
                    height: Math.max(barHeight, 4),
                    backgroundColor: color,
                    opacity: 0.15 + (val / maxVal) * 0.85,
                  },
                ]}
              />
              <Text style={miniChartStyles.barLabel}>
                {labels[i] ?? ''}
              </Text>
            </View>
          );
        })}
      </View>
    </View>
  );
};

const miniChartStyles = StyleSheet.create({
  container: {
    paddingTop: 10,
  },
  barsRow: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    justifyContent: 'space-between',
    height: 160,
    paddingBottom: 24,
  },
  barWrapper: {
    flex: 1,
    alignItems: 'center',
    marginHorizontal: 2,
  },
  bar: {
    width: '65%',
    borderRadius: 6,
    minWidth: 8,
  },
  barLabel: {
    fontSize: 10,
    color: lightColors.subtext,
    marginTop: 6,
    textAlign: 'center',
  },
});

// ════════════════════════════════════════════════════════════════════════════
// Ana HomeScreen Bileşeni
// ════════════════════════════════════════════════════════════════════════════
const HomeScreen = () => {
  const user = useSelector((state: RootState) => state.auth.user);
  const [refreshing, setRefreshing] = useState(false);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [allTasks, setAllTasks] = useState<Task[]>([]);
  const [sales, setSales] = useState<Sale[]>([]);
  const navigation =
    useNavigation<BottomTabNavigationProp<MainTabParamList>>();

  // ───── Veri Çekme ─────
  const fetchData = async () => {
    try {
      // Müşterileri getir
      const data = await customerAPI.getAll();
      setCustomers(Array.isArray(data) ? data : []);

      // Görevleri getir
      const tasksResponse: any = await taskAPI.getAll();
      let tasksList: Task[] = [];
      if (tasksResponse?.data?.data) {
        tasksList = tasksResponse.data.data;
      } else if (Array.isArray(tasksResponse?.data)) {
        tasksList = tasksResponse.data;
      } else if (Array.isArray(tasksResponse)) {
        tasksList = tasksResponse;
      }
      setAllTasks(tasksList);

      const todayTasks = tasksList.filter((task: Task) => {
        if (!task.dueDate) return false;
        const taskDate = new Date(task.dueDate).toDateString();
        const today = new Date().toDateString();
        return taskDate === today;
      });
      setTasks(todayTasks.slice(0, 5));

      // Satış verilerini getir
      const salesResponse: any = await salesAPI.getAll();
      let salesList: Sale[] = [];
      if (salesResponse) {
        if (Array.isArray(salesResponse)) {
          salesList = salesResponse;
        } else if (Array.isArray(salesResponse?.data)) {
          salesList = salesResponse.data;
        } else if (Array.isArray(salesResponse?.data?.data)) {
          salesList = salesResponse.data.data;
        }
      }
      setSales(salesList);
    } catch (error: any) {
      console.error('Data fetching error:', error?.message);
      setCustomers([]);
      setTasks([]);
      setAllTasks([]);
      setSales([]);
    }
  };

  useEffect(() => {
    fetchData();
  }, [user]);

  const onRefresh = useCallback(() => {
    setRefreshing(true);
    fetchData().finally(() => setRefreshing(false));
  }, []);

  const handleProfilePress = () => {
    navigation.navigate('Settings' as any);
  };

  // ───── Hesaplamalar ─────
  const customerCount = useMemo(() => {
    return Array.isArray(customers) ? customers.length : 0;
  }, [customers]);

  const totalSales = useMemo(() => {
    return sales.reduce((acc, curr) => acc + (curr.amount || 0), 0);
  }, [sales]);

  const completedTasksCount = useMemo(() => {
    return allTasks.filter(t => t.status === 'completed').length;
  }, [allTasks]);

  const formatNumber = (num: number): string => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(0)}K`;
    return num.toString();
  };

  // Satış verilerini aylık gruplandırma
  const monthlySalesData = useMemo(() => {
    if (!sales || sales.length === 0) {
      return {data: [0], labels: ['—']};
    }

    const monthMap: {[key: string]: number} = {};
    const monthLabels = [
      'Oca',
      'Şub',
      'Mar',
      'Nis',
      'May',
      'Haz',
      'Tem',
      'Ağu',
      'Eyl',
      'Eki',
      'Kas',
      'Ara',
    ];

    sales.forEach(sale => {
      if (!sale.date || !sale.amount) return;
      const d = new Date(sale.date);
      const key = `${d.getFullYear()}-${d.getMonth()}`;
      monthMap[key] = (monthMap[key] || 0) + sale.amount;
    });

    const sortedKeys = Object.keys(monthMap).sort();
    const last6 = sortedKeys.slice(-6);

    if (last6.length === 0) return {data: [0], labels: ['—']};

    return {
      data: last6.map(k => monthMap[k] / 1000), // Binlik
      labels: last6.map(k => {
        const monthIndex = parseInt(k.split('-')[1]);
        return monthLabels[monthIndex] ?? '';
      }),
    };
  }, [sales]);

  // Kullanıcının baş harfi
  const userInitial = user?.name ? user.name.charAt(0).toUpperCase() : 'S';

  // Son aktiviteler — gerçek veriden türetiliyor, dummy yok
  const recentActivities = useMemo(() => {
    const activities: {icon: string; title: string; time: string}[] = [];

    // Son eklenen görevler
    const sortedTasks = [...allTasks]
      .filter(t => t.dueDate)
      .sort(
        (a, b) =>
          new Date(b.dueDate).getTime() - new Date(a.dueDate).getTime(),
      );

    sortedTasks.slice(0, 2).forEach(task => {
      const dueDate = new Date(task.dueDate);
      const now = new Date();
      const diffMs = now.getTime() - dueDate.getTime();
      const diffHours = Math.max(1, Math.floor(diffMs / (1000 * 60 * 60)));
      const timeStr =
        diffHours < 24
          ? `${diffHours} saat önce`
          : `${Math.floor(diffHours / 24)} gün önce`;

      activities.push({
        icon:
          task.status === 'completed'
            ? 'check-circle-outline'
            : 'clipboard-text-outline',
        title: task.title,
        time: timeStr,
      });
    });

    // Boşsa bilgilendirme
    if (activities.length === 0) {
      activities.push({
        icon: 'information-outline',
        title: 'Henüz aktivite bulunmuyor',
        time: 'Görev oluşturun',
      });
    }

    return activities;
  }, [allTasks]);

  // ───── Render ─────
  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView
        style={styles.container}
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }>
        {/* ─── Header ─── */}
        <View style={styles.header}>
          <View style={styles.headerLeft}>
            <Text style={styles.welcomeText}>Hoş geldiniz,</Text>
            <Text style={styles.nameText}>{user?.name ?? 'Kullanıcı'}</Text>
          </View>
          <TouchableOpacity
            onPress={handleProfilePress}
            style={styles.avatarContainer}
            activeOpacity={0.7}>
            <View style={styles.avatar}>
              <Text style={styles.avatarText}>{userInitial}</Text>
            </View>
          </TouchableOpacity>
        </View>

        {/* ─── İstatistik Kartları ─── */}
        <View style={styles.statsRow}>
          <StatCard
            icon="account-group-outline"
            value={customerCount}
            label="Müşteri"
            gradient={['#0EA5E9', '#0284C7']}
            accentColor="#0EA5E9"
          />
          <StatCard
            icon="clipboard-check-outline"
            value={completedTasksCount}
            label="Tamamlanan"
            gradient={['#10B981', '#059669']}
            accentColor="#10B981"
          />
          <StatCard
            icon="trending-up"
            value={`₺${formatNumber(totalSales)}`}
            label="Toplam Satış"
            gradient={['#6366F1', '#4F46E5']}
            accentColor="#6366F1"
          />
        </View>

        {/* ─── Oyunlaştırma (Saha Ligi) Banner ─── */}
        <TouchableOpacity 
          style={styles.gamificationBanner}
          activeOpacity={0.85}
          onPress={() => navigation.navigate('Gamification' as any)}>
          <View style={styles.gamificationHeader}>
            <View style={styles.gamificationTitleBox}>
              <Icon name="trophy" size={24} color="#F59E0B" />
              <Text style={styles.gamificationTitle}>Saha Ligi & Rozetler 🏆</Text>
            </View>
            <View style={styles.streakPill}>
              <Icon name="fire" size={16} color="#FF5722" />
              <Text style={styles.streakPillText}>Seri 🔥</Text>
            </View>
          </View>
          <Text style={styles.gamificationSubtitle}>
            GPS doğrulamalı ziyaretler yaparak XP kazan, gizli ligde yüksel ve rozetleri topla!
          </Text>
          <View style={styles.gamificationFooter}>
            <Text style={styles.gamificationBtnText}>Liderlik Tablosunu Gör →</Text>
          </View>
        </TouchableOpacity>

        {/* ─── Satış Grafiği ─── */}
        <Card style={styles.chartCard}>
          <Card.Content>
            <View style={styles.cardHeader}>
              <View>
                <Text style={styles.cardTitle}>Satış İstatistikleri</Text>
                <Text style={styles.cardSubtitle}>Son 6 ay (₺ Bin)</Text>
              </View>
              <View style={styles.chartBadge}>
                <Icon name="chart-bar" size={16} color={lightColors.primary} />
              </View>
            </View>
            <MiniBarChart
              data={monthlySalesData.data}
              labels={monthlySalesData.labels}
              color={lightColors.primary}
            />
          </Card.Content>
        </Card>

        {/* ─── Bugünkü Görevler ─── */}
        <Card style={styles.sectionCard}>
          <Card.Content>
            <View style={styles.cardHeader}>
              <Text style={styles.cardTitle}>Bugünkü Görevler</Text>
              <TouchableOpacity onPress={() => navigation.navigate('Tasks')}>
                <Text style={styles.seeAllText}>Tümünü Gör →</Text>
              </TouchableOpacity>
            </View>

            {tasks.length === 0 ? (
              <View style={styles.emptyState}>
                <Icon
                  name="calendar-blank-outline"
                  size={36}
                  color={lightColors.disabled}
                />
                <Text style={styles.emptyText}>
                  Bugün için planlanmış görev yok
                </Text>
              </View>
            ) : (
              tasks.map(task => (
                <View key={task.id} style={styles.taskItem}>
                  <View style={styles.taskRow}>
                    <View style={styles.taskLeft}>
                      <View
                        style={[
                          styles.taskDot,
                          {
                            backgroundColor:
                              task.priority === 'high'
                                ? lightColors.error
                                : task.priority === 'medium'
                                ? lightColors.warning
                                : lightColors.success,
                          },
                        ]}
                      />
                      <Text
                        style={styles.taskTitle}
                        numberOfLines={1}
                        ellipsizeMode="tail">
                        {task.title}
                      </Text>
                    </View>
                    <Text style={styles.taskTime}>
                      {task.dueDate
                        ? new Date(task.dueDate).toLocaleTimeString('tr-TR', {
                            hour: '2-digit',
                            minute: '2-digit',
                          })
                        : ''}
                    </Text>
                  </View>
                  <ProgressBar
                    progress={
                      task.status === 'completed'
                        ? 1
                        : task.progress
                        ? task.progress / 100
                        : task.status === 'in_progress'
                        ? 0.5
                        : 0.1
                    }
                    color={
                      task.status === 'completed'
                        ? lightColors.success
                        : lightColors.primary
                    }
                    style={{marginTop: 8, marginLeft: 18}}
                  />
                </View>
              ))
            )}
          </Card.Content>
        </Card>

        {/* ─── Son Aktiviteler — Gerçek Veriden ─── */}
        <Card style={[styles.sectionCard, {marginBottom: 32}]}>
          <Card.Content>
            <Text style={styles.cardTitle}>Son Aktiviteler</Text>
            {recentActivities.map((activity, index) => (
              <View key={index} style={styles.activityItem}>
                <View style={styles.activityIconCircle}>
                  <Icon
                    name={activity.icon as any}
                    size={18}
                    color={lightColors.primary}
                  />
                </View>
                <View style={styles.activityInfo}>
                  <Text style={styles.activityTitle} numberOfLines={1}>
                    {activity.title}
                  </Text>
                  <Text style={styles.activityTime}>{activity.time}</Text>
                </View>
              </View>
            ))}
          </Card.Content>
        </Card>
      </ScrollView>
    </SafeAreaView>
  );
};

// ════════════════════════════════════════════════════════════════════════════
// Stiller
// ════════════════════════════════════════════════════════════════════════════
const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: lightColors.background,
  },
  container: {
    flex: 1,
    backgroundColor: lightColors.background,
  },
  // Header
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
  },
  headerLeft: {
    flex: 1,
  },
  welcomeText: {
    fontSize: 15,
    color: lightColors.subtext,
    fontWeight: '400',
  },
  nameText: {
    fontSize: 24,
    fontWeight: '700',
    color: lightColors.primary,
    marginTop: 2,
  },
  avatarContainer: {
    marginLeft: spacing.md,
  },
  avatar: {
    width: 52,
    height: 52,
    borderRadius: 26,
    backgroundColor: lightColors.primary,
    alignItems: 'center',
    justifyContent: 'center',
    ...shadows.small,
  },
  avatarText: {
    fontSize: 22,
    fontWeight: '700',
    color: '#FFFFFF',
  },
  // Stats
  statsRow: {
    flexDirection: 'row',
    paddingHorizontal: spacing.md,
    marginBottom: spacing.md,
  },
  // Chart Card
  chartCard: {
    marginHorizontal: spacing.md,
    marginBottom: spacing.md,
  },
  chartBadge: {
    width: 34,
    height: 34,
    borderRadius: 10,
    backgroundColor: `${lightColors.primary}12`,
    alignItems: 'center',
    justifyContent: 'center',
  },
  // Section Card
  sectionCard: {
    marginHorizontal: spacing.md,
    marginBottom: spacing.md,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  cardTitle: {
    fontSize: 17,
    fontWeight: '700',
    color: lightColors.text,
  },
  cardSubtitle: {
    fontSize: 12,
    color: lightColors.subtext,
    marginTop: 2,
  },
  seeAllText: {
    fontSize: 13,
    color: lightColors.primary,
    fontWeight: '600',
  },
  // Tasks
  taskItem: {
    paddingVertical: 10,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: lightColors.border,
  },
  taskRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  taskLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
    marginRight: spacing.sm,
  },
  taskDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 10,
  },
  taskTitle: {
    fontSize: 14,
    fontWeight: '500',
    color: lightColors.text,
    flex: 1,
  },
  taskTime: {
    fontSize: 12,
    color: lightColors.subtext,
  },
  // Empty State
  emptyState: {
    alignItems: 'center',
    paddingVertical: 24,
    gap: 8,
  },
  emptyText: {
    fontSize: 13,
    color: lightColors.subtext,
  },
  // Activities
  activityItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 14,
  },
  activityIconCircle: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: `${lightColors.primary}12`,
    alignItems: 'center',
    justifyContent: 'center',
  },
  activityInfo: {
    marginLeft: 12,
    flex: 1,
  },
  activityTitle: {
    fontSize: 14,
    fontWeight: '500',
    color: lightColors.text,
  },
  activityTime: {
    fontSize: 12,
    color: lightColors.subtext,
    marginTop: 2,
  },
  // Gamification Banner Styles (Brand Cyan Theme)
  gamificationBanner: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 16,
    marginHorizontal: 16,
    marginBottom: 16,
    borderWidth: 1.5,
    borderColor: '#0EA5E9',
    elevation: 3,
    shadowColor: '#0EA5E9',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.12,
    shadowRadius: 6,
  },
  gamificationHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  gamificationTitleBox: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  gamificationTitle: {
    color: '#0F172A',
    fontSize: 16,
    fontWeight: '700',
  },
  streakPill: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FEF2F2',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
    gap: 4,
  },
  streakPillText: {
    color: '#EF4444',
    fontSize: 12,
    fontWeight: '700',
  },
  gamificationSubtitle: {
    color: '#64748B',
    fontSize: 13,
    marginTop: 8,
    lineHeight: 18,
  },
  gamificationFooter: {
    marginTop: 12,
    alignSelf: 'flex-start',
  },
  gamificationBtnText: {
    color: '#0EA5E9',
    fontSize: 14,
    fontWeight: '700',
  },
});

export default HomeScreen;
