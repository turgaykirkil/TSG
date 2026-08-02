import React, { useMemo } from 'react';
import { View, StyleSheet, ScrollView, TouchableOpacity, Text, ActivityIndicator } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { TaskStackNavigationProp } from '../../navigation/types';
import { Task, formatDate, getPriorityColor } from '../../types/task';
import { MaterialCommunityIcons } from '@expo/vector-icons';

interface TaskListContentProps {
  tasks: Task[];
  loading: boolean;
  searchQuery: string;
  selectedFilter: string | null;
}

const TaskListContent: React.FC<TaskListContentProps> = ({
  tasks,
  loading,
  searchQuery,
  selectedFilter,
}) => {
  const navigation = useNavigation<TaskStackNavigationProp>();

  const filteredTasks = useMemo(() => {
    return tasks.filter((task) => {
      const matchesSearch =
        task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        task.description.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesFilter = !selectedFilter || task.status === selectedFilter;
      return matchesSearch && matchesFilter;
    });
  }, [tasks, searchQuery, selectedFilter]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return '#10B981';
      case 'in_progress':
        return '#00A0E9';
      default:
        return '#F59E0B';
    }
  };

  if (loading) {
    return (
      <View style={styles.emptyContainer}>
        <ActivityIndicator size="large" color="#00A0E9" />
      </View>
    );
  }

  if (filteredTasks.length === 0) {
    return (
      <View style={styles.emptyContainer}>
        <MaterialCommunityIcons
          name="clipboard-text-outline"
          size={56}
          color="#9CA3AF"
          style={styles.emptyIcon}
        />
        <Text style={styles.emptyText}>
          {searchQuery || selectedFilter
            ? 'Arama sonucu bulunamadı'
            : 'Henüz görev eklenmemiş'}
        </Text>
      </View>
    );
  }

  return (
    <ScrollView
      contentContainerStyle={styles.taskListContainer}
      showsVerticalScrollIndicator={false}
    >
      {filteredTasks.map((task) => (
        <TouchableOpacity
          key={task.id}
          style={styles.taskItem}
          activeOpacity={0.7}
          onPress={() => navigation.navigate('TaskDetail', { taskId: task.id })}
        >
          <View style={styles.taskHeader}>
            <Text style={styles.taskTitle} numberOfLines={1}>
              {task.title}
            </Text>
            <View
              style={[
                styles.priorityBadge,
                { backgroundColor: getPriorityColor(task.priority) || '#E0F2FE' },
              ]}
            >
              <Text style={styles.priorityText}>{task.priority}</Text>
            </View>
          </View>
          <Text style={styles.taskDescription} numberOfLines={2}>
            {task.description}
          </Text>
          <View style={styles.taskFooter}>
            <Text style={styles.taskDate}>{formatDate(task.dueDate)}</Text>
            <View style={styles.statusContainer}>
              <View
                style={[
                  styles.statusDot,
                  { backgroundColor: getStatusColor(task.status) },
                ]}
              />
              <Text style={styles.statusText}>
                {task.status === 'in_progress'
                  ? 'Devam Ediyor'
                  : task.status === 'completed'
                  ? 'Tamamlandı'
                  : 'Bekliyor'}
              </Text>
            </View>
          </View>
        </TouchableOpacity>
      ))}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  taskListContainer: {
    paddingVertical: 8,
  },
  taskItem: {
    backgroundColor: '#FFFFFF',
    marginHorizontal: 16,
    marginVertical: 6,
    padding: 14,
    borderRadius: 12,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.08,
    shadowRadius: 2,
  },
  taskHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 6,
  },
  taskTitle: {
    fontSize: 15,
    fontWeight: 'bold',
    color: '#1F2937',
    flex: 1,
    marginRight: 8,
  },
  priorityBadge: {
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 10,
  },
  priorityText: {
    fontSize: 11,
    fontWeight: '600',
    color: '#FFFFFF',
  },
  taskDescription: {
    fontSize: 13,
    color: '#4B5563',
    marginBottom: 10,
    lineHeight: 18,
  },
  taskFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderTopWidth: StyleSheet.hairlineWidth,
    borderTopColor: '#F3F4F6',
    paddingTop: 8,
  },
  taskDate: {
    fontSize: 12,
    color: '#6B7280',
    fontWeight: '500',
  },
  statusContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 6,
  },
  statusText: {
    fontSize: 12,
    color: '#374151',
    fontWeight: '500',
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
    minHeight: 200,
  },
  emptyText: {
    fontSize: 15,
    color: '#6B7280',
    textAlign: 'center',
    marginTop: 8,
  },
  emptyIcon: {
    marginBottom: 12,
  },
});

export default TaskListContent;
