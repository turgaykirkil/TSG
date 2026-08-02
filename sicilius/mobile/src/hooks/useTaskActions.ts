import { useState } from 'react';
import { Alert } from 'react-native';
import { useDispatch } from 'react-redux';
import { AppDispatch } from '../store/store';
type TaskStatus = 'todo' | 'in_progress' | 'completed';
import { updateTaskStatus, updateTaskProgress, updateChecklistItem, deleteTask } from '../store/slices/taskSlice';

interface MenuAnchor {
  x: number;
  y: number;
}

export const useTaskActions = (taskId: string) => {
  const dispatch = useDispatch<AppDispatch>();
  const [menuVisible, setMenuVisible] = useState(false);
  const [menuAnchor, setMenuAnchor] = useState<MenuAnchor>({ x: 0, y: 0 });
  const [deleteDialogVisible, setDeleteDialogVisible] = useState(false);
  const [progressDialogVisible, setProgressDialogVisible] = useState(false);
  const [progress, setProgress] = useState('0');

  const handleStatusChange = async (newStatus: TaskStatus) => {
    try {
      await dispatch(
        updateTaskStatus({id: taskId, status: newStatus}),
      ).unwrap();
      setMenuVisible(false);
    } catch (error) {
      Alert.alert('Error', 'Failed to update status');
    }
  };

  const handleProgressUpdate = async () => {
    const progressValue = parseInt(progress);
    if (isNaN(progressValue) || progressValue < 0 || progressValue > 100) {
      Alert.alert('Error', 'Please enter a valid progress value (0-100)');
      return;
    }

    try {
      await dispatch(
        updateTaskProgress({id: taskId, progress: progressValue}),
      ).unwrap();
      setProgressDialogVisible(false);
    } catch (error) {
      Alert.alert('Error', 'Failed to update progress');
    }
  };

  const handleChecklistItemToggle = async (itemId: string) => {
    try {
      await dispatch(
        updateChecklistItem({taskId, itemId, completed: true}),
      ).unwrap();
    } catch (error) {
      Alert.alert('Error', 'Failed to update checklist item');
    }
  };

  const handleDelete = async () => {
    try {
      await dispatch(deleteTask(taskId)).unwrap();
      return true;
    } catch (error) {
      Alert.alert('Error', 'Failed to delete task');
      return false;
    }
  };

  const showMenu = (event: any) => {
    const { pageX, pageY } = event.nativeEvent;
    setMenuAnchor({ x: pageX, y: pageY });
    setMenuVisible(true);
  };

  return {
    menuVisible,
    setMenuVisible,
    menuAnchor,
    showMenu,
    deleteDialogVisible,
    setDeleteDialogVisible,
    progressDialogVisible,
    setProgressDialogVisible,
    progress,
    setProgress,
    handleStatusChange,
    handleProgressUpdate,
    handleChecklistItemToggle,
    handleDelete
  };
};
