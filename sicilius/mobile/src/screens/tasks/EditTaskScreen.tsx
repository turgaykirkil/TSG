import React, { useEffect } from 'react';
import { View, ScrollView, StyleSheet, Text, TouchableOpacity, ActivityIndicator } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RouteProp } from '@react-navigation/native';
import { Formik } from 'formik';
import * as Yup from 'yup';

import { TaskStackParamList } from '../../navigation/types';
import { Task } from '../../types/task';
import { fetchTaskById, updateTask } from '../../store/slices/taskSlice';
import { RootState, AppDispatch } from '../../store';

import EditTaskForm from '../../components/tasks/EditTaskForm';
import EditTaskPrioritySelect from '../../components/tasks/EditTaskPrioritySelect';
import EditTaskStatusSelect from '../../components/tasks/EditTaskStatusSelect';
import EditTaskDatePicker from '../../components/tasks/EditTaskDatePicker';
import EditTaskChecklist from '../../components/tasks/EditTaskChecklist';
import { lightColors } from '../../theme';

type EditTaskScreenProps = {
  navigation: NativeStackNavigationProp<TaskStackParamList, 'EditTask'>;
  route: RouteProp<TaskStackParamList, 'EditTask'>;
};

const validationSchema = Yup.object().shape({
  title: Yup.string().required('Başlık gereklidir'),
  description: Yup.string(),
  dueDate: Yup.date().required('Son tarih gereklidir'),
  priority: Yup.string().oneOf(['low', 'medium', 'high'], 'Geçersiz öncelik').required('Öncelik gereklidir'),
  status: Yup.string().oneOf(['todo', 'in_progress', 'completed'], 'Geçersiz durum').required('Durum gereklidir'),
  checklist: Yup.array().of(
    Yup.object().shape({
      id: Yup.string().required(),
      title: Yup.string().required(),
      completed: Yup.boolean().required()
    })
  )
});

const EditTaskScreen: React.FC<EditTaskScreenProps> = ({ navigation, route }) => {
  const dispatch = useDispatch<AppDispatch>();
  const { taskId } = route.params;
  const { selectedTask: task, loading } = useSelector((state: RootState) => state.tasks);

  useEffect(() => {
    dispatch(fetchTaskById(taskId));
  }, [taskId]);

  const handleSubmit = async (values: Task) => {
    try {
      await dispatch(updateTask({ id: taskId, updates: values }) as any);
      navigation.goBack();
    } catch (error) {
      console.error('Görev güncellenirken hata:', error);
    }
  };

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color={lightColors.primary} />
      </View>
    );
  }

  if (!task) {
    return (
      <View style={styles.centered}>
        <Text style={styles.emptyText}>Görev bulunamadı.</Text>
      </View>
    );
  }

  return (
    <Formik
      initialValues={task}
      validationSchema={validationSchema}
      onSubmit={handleSubmit}
    >
      {(formik) => (
        <ScrollView 
          contentContainerStyle={styles.container}
          showsVerticalScrollIndicator={false}
        >
          <EditTaskForm formik={formik} />
          <EditTaskPrioritySelect formik={formik} />
          <EditTaskStatusSelect formik={formik} />
          <EditTaskDatePicker formik={formik} />
          <EditTaskChecklist formik={formik} />
          
          <TouchableOpacity
            style={[
              styles.submitButton,
              (!formik.isValid || formik.isSubmitting) && styles.disabledButton
            ]}
            onPress={() => formik.handleSubmit()}
            disabled={!formik.isValid || formik.isSubmitting}
          >
            {formik.isSubmitting ? (
              <ActivityIndicator color="#FFFFFF" size="small" />
            ) : (
              <Text style={styles.submitButtonText}>Görevi Güncelle</Text>
            )}
          </TouchableOpacity>
        </ScrollView>
      )}
    </Formik>
  );
};

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    padding: 16,
    backgroundColor: lightColors.background,
  },
  submitButton: {
    marginTop: 24,
    marginBottom: 16,
    height: 48,
    borderRadius: 8,
    backgroundColor: lightColors.primary,
    justifyContent: 'center',
    alignItems: 'center',
  },
  disabledButton: {
    opacity: 0.6,
  },
  submitButtonText: {
    color: '#FFFFFF',
    fontWeight: 'bold',
    fontSize: 15,
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: lightColors.background,
  },
  emptyText: {
    color: lightColors.subtext,
    fontSize: 14,
  },
});

export default EditTaskScreen;
