import React, { useState, useEffect } from 'react';
import { View, StyleSheet, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { TaskStackNavigationProp } from '../../navigation/types';
import { taskAPI } from '../../services/api';
import { Task } from '../../types/task';
import { lightColors } from '../../theme';

import TaskListHeader from '../../components/tasks/TaskListHeader';
import TaskListContent from '../../components/tasks/TaskListContent';
import TaskListFAB from '../../components/tasks/TaskListFAB';

const TaskListScreen: React.FC = () => {
  const navigation = useNavigation<TaskStackNavigationProp>();

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFilter, setSelectedFilter] = useState<string | null>(null);
  const [localTasks, setLocalTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        setIsLoading(true);
        const data = await taskAPI.getAll();
        setLocalTasks(data);
      } catch (error) {
        Alert.alert('Hata', 'Görevler yüklenemedi');
      } finally {
        setIsLoading(false);
      }
    };

    fetchTasks();
  }, []);

  const handleFilterChange = (filter: string | null) => {
    setSelectedFilter(prevFilter => 
      prevFilter === filter ? null : filter
    );
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.container}>
        <TaskListHeader
          searchQuery={searchQuery}
          onSearchChange={setSearchQuery}
          selectedFilter={selectedFilter}
          onFilterChange={handleFilterChange}
        />
        <TaskListContent
          tasks={localTasks}
          loading={isLoading}
          searchQuery={searchQuery}
          selectedFilter={selectedFilter}
        />
        <TaskListFAB />
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: lightColors.background,
  },
  container: {
    flex: 1,
    backgroundColor: lightColors.background,
  },
});

export default TaskListScreen;