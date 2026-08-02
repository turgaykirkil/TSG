import React, { useMemo } from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { NativeStackNavigationOptions } from '@react-navigation/native-stack';

import TaskListScreen from '../screens/tasks/TaskListScreen';
import TaskDetailScreen from '../screens/tasks/TaskDetailScreen';
import NewTaskScreen from '../screens/tasks/NewTaskScreen';
import EditTaskScreen from '../screens/tasks/EditTaskScreen';
import { TaskStackParamList } from './types';
import { lightColors } from '../theme';

const Stack = createNativeStackNavigator<TaskStackParamList>();

// Sabit ekran konfigürasyonları
const TASK_SCREEN_CONFIG = Object.freeze({
  TaskList: {
    title: 'Görevler',
    component: TaskListScreen
  },
  TaskDetail: {
    title: 'Görev Detayı',
    component: TaskDetailScreen
  },
  NewTask: {
    title: 'Yeni Görev',
    component: NewTaskScreen
  },
  EditTask: {
    title: 'Görevi Düzenle',
    component: EditTaskScreen
  }
});

const TaskNavigator = React.memo(() => {
  // Navigator seçeneklerini memoize et
  const navigatorScreenOptions = useMemo<NativeStackNavigationOptions>(() => ({
    headerStyle: {
      backgroundColor: lightColors.primary,
    },
    headerTintColor: '#fff',
    headerTitleStyle: {
      fontWeight: 'bold',
    },
    // Performans için ek ayarlar
    animation: 'slide_from_right',
    gestureEnabled: true,
    detachInactiveScreens: true
  }), []);

  // Ekran tanımlamalarını memoize et
  const TaskScreens = useMemo(() => (
    Object.entries(TASK_SCREEN_CONFIG).map(([name, config]) => (
      <Stack.Screen
        key={name}
        name={name as keyof TaskStackParamList}
        component={config.component}
        options={{
          title: config.title,
        }}
      />
    ))
  ), []);

  return (
    <Stack.Navigator
      screenOptions={navigatorScreenOptions}
    >
      {TaskScreens}
    </Stack.Navigator>
  );
});

export default TaskNavigator;
