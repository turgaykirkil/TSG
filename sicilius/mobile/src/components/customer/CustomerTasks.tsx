import React, { memo } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { MaterialCommunityIcons as Icon } from '@expo/vector-icons';
import { Customer } from '../../types/customer';
import { lightColors } from '../../theme';

interface CustomerTasksProps {
  customer: Customer | null;
  onSeeAll?: () => void;
}

const CustomerTasks = memo<CustomerTasksProps>(({ customer, onSeeAll }) => {
  const tasks = (customer as any)?.assignedTasks;

  return (
    <View style={styles.container}>
      <View style={styles.sectionHeader}>
        <Text style={styles.sectionTitle}>Görevler</Text>
        <TouchableOpacity onPress={onSeeAll}>
          <Text style={styles.seeAllText}>Tümünü Gör</Text>
        </TouchableOpacity>
      </View>

      {Array.isArray(tasks) && tasks.length > 0 ? (
        tasks.map((task: any) => (
          <View key={task.id} style={styles.taskItem}>
            <Icon
              name={task.status === 'completed' ? 'checkbox-marked-circle' : 'clock-outline'}
              size={20}
              color={task.status === 'completed' ? '#10B981' : lightColors.primary}
            />
            <View style={styles.taskInfo}>
              <Text style={styles.taskTitle}>{task.title}</Text>
              <Text style={styles.taskDate}>Son Tarih: {task.dueDate}</Text>
            </View>
          </View>
        ))
      ) : (
        <Text style={styles.emptyText}>Atanmış görev bulunmuyor</Text>
      )}
    </View>
  );
});

const styles = StyleSheet.create({
  container: {
    paddingVertical: 4,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: lightColors.text,
  },
  seeAllText: {
    fontSize: 14,
    color: lightColors.primary,
    fontWeight: '600',
  },
  taskItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 6,
  },
  taskInfo: {
    flex: 1,
    marginLeft: 12,
  },
  taskTitle: {
    fontSize: 14,
    fontWeight: '500',
    color: lightColors.text,
  },
  taskDate: {
    fontSize: 12,
    color: lightColors.subtext,
    marginTop: 2,
  },
  emptyText: {
    fontSize: 13,
    color: lightColors.subtext,
    textAlign: 'center',
    paddingVertical: 8,
  },
});

CustomerTasks.displayName = 'CustomerTasks';

export default CustomerTasks;
