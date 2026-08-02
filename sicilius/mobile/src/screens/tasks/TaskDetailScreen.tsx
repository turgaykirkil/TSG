import React from 'react';
import { View, StyleSheet, ScrollView, Text, TouchableOpacity, ActivityIndicator, Modal } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { useTaskDetail } from '../../hooks/useTaskDetail';
import { useTaskActions } from '../../hooks/useTaskActions';
import { TaskHeader } from '../../components/task/TaskHeader';
import { TaskDetails } from '../../components/task/TaskDetails';
import { getDisplayValue } from '../../utils/display';

import TaskDeleteDialog from '../../components/tasks/TaskDeleteDialog';
import TaskProgressDialog from '../../components/tasks/TaskProgressDialog';
import { lightColors } from '../../theme';

const TaskDetailScreen: React.FC<any> = ({ route }) => {
  const taskId = route?.params?.taskId;
  const navigation = useNavigation<any>();
  
  const { task, error, loading } = useTaskDetail({ taskId });
  const {
    menuVisible,
    setMenuVisible,
    showMenu,
    deleteDialogVisible,
    setDeleteDialogVisible,
    progressDialogVisible,
    setProgressDialogVisible,
    progress,
    setProgress,
    handleStatusChange,
    handleProgressUpdate,
    handleDelete
  } = useTaskActions(taskId);

  const handleCustomerPress = (customerId: string) => {
    navigation.navigate('Customers', {
      screen: 'CustomerDetail',
      params: { customerId },
    });
  };

  const onDeleteConfirm = async () => {
    const success = await handleDelete();
    if (success) {
      navigation.goBack();
    }
  };

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color={lightColors.primary} />
        <Text style={styles.loadingText}>Görev yükleniyor...</Text>
      </View>
    );
  }

  if (error || !task) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.errorText}>
          {error || 'Görev bulunamadı'}
        </Text>
        <TouchableOpacity 
          style={styles.errorButton}
          onPress={() => navigation.goBack()}
        >
          <Text style={styles.errorButtonText}>Geri Dön</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false}>
        <TaskHeader
          title={getDisplayValue(task.title)}
          status={getDisplayValue(task.status)}
          priority={getDisplayValue(task.priority)}
          onMenuPress={showMenu}
        />

        <TaskDetails
          description={getDisplayValue(task.description)}
          priority={getDisplayValue(task.priority)}
          dueDate={typeof task.dueDate === 'string' ? task.dueDate : task.dueDate ? new Date(task.dueDate).toLocaleDateString('tr-TR') : ''}
          customerName={getDisplayValue(task.customerName)}
          onCustomerPress={() => handleCustomerPress(task.customerId)}
        />
      </ScrollView>

      <Modal
        visible={menuVisible}
        transparent
        animationType="fade"
        onRequestClose={() => setMenuVisible(false)}
      >
        <TouchableOpacity style={styles.modalOverlay} activeOpacity={1} onPress={() => setMenuVisible(false)}>
          <View style={styles.menuContainer}>
            <TouchableOpacity 
              style={styles.menuItem}
              onPress={() => {
                setMenuVisible(false);
                setProgressDialogVisible(true);
              }}
            >
              <Text style={styles.menuItemText}>İlerleme Güncelle</Text>
            </TouchableOpacity>
            <TouchableOpacity 
              style={styles.menuItem}
              onPress={() => handleStatusChange('completed')}
            >
              <Text style={styles.menuItemText}>Tamamlandı</Text>
            </TouchableOpacity>
            <TouchableOpacity 
              style={styles.menuItem}
              onPress={() => handleStatusChange('in_progress')}
            >
              <Text style={styles.menuItemText}>Devam Ediyor</Text>
            </TouchableOpacity>
            <TouchableOpacity 
              style={[styles.menuItem, styles.deleteMenuItem]}
              onPress={() => {
                setMenuVisible(false);
                setDeleteDialogVisible(true);
              }}
            >
              <Text style={styles.deleteMenuItemText}>Sil</Text>
            </TouchableOpacity>
          </View>
        </TouchableOpacity>
      </Modal>

      <TaskDeleteDialog
        visible={deleteDialogVisible}
        onDismiss={() => setDeleteDialogVisible(false)}
        onDelete={onDeleteConfirm}
        taskTitle={task.title}
      />

      <TaskProgressDialog
        visible={progressDialogVisible}
        onDismiss={() => setProgressDialogVisible(false)}
        onUpdate={handleProgressUpdate}
        progress={progress}
        onProgressChange={setProgress}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: lightColors.background,
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 16,
    backgroundColor: lightColors.background,
  },
  loadingText: {
    marginTop: 16,
    color: lightColors.subtext,
  },
  errorText: {
    textAlign: 'center',
    marginBottom: 16,
    fontSize: 16,
    color: lightColors.error,
  },
  errorButton: {
    marginTop: 16,
    backgroundColor: lightColors.primary,
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
  },
  errorButtonText: {
    color: '#FFFFFF',
    fontWeight: 'bold',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.4)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  menuContainer: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    paddingVertical: 8,
    width: '80%',
    maxWidth: 280,
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.15,
    shadowRadius: 6,
  },
  menuItem: {
    paddingVertical: 12,
    paddingHorizontal: 16,
  },
  menuItemText: {
    fontSize: 15,
    color: lightColors.text,
  },
  deleteMenuItem: {
    borderTopWidth: 1,
    borderTopColor: lightColors.border,
  },
  deleteMenuItemText: {
    fontSize: 15,
    color: lightColors.error,
    fontWeight: 'bold',
  },
});

export default TaskDetailScreen;
