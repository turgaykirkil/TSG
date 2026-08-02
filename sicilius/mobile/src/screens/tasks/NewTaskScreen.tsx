import React from 'react';
import { ScrollView, StyleSheet, Platform, TouchableOpacity, Text, ActivityIndicator } from 'react-native';
import { Formik } from 'formik';
import * as Yup from 'yup';

import NewTaskForm from '../../components/tasks/NewTaskForm';
import NewTaskCustomerSelect from '../../components/tasks/NewTaskCustomerSelect';
import NewTaskAssigneeSelect from '../../components/tasks/NewTaskAssigneeSelect';
import NewTaskPrioritySelect from '../../components/tasks/NewTaskPrioritySelect';
import NewTaskDatePicker from '../../components/tasks/NewTaskDatePicker';
import NewTaskChecklist from '../../components/tasks/NewTaskChecklist';

import { TaskFormValues } from '../../types/task';
import { createTask } from '../../store/slices/taskSlice';
import { lightColors } from '../../theme';

const validationSchema = Yup.object().shape({
  title: Yup.string().required('Başlık gereklidir'),
  description: Yup.string(),
  customerId: Yup.string().required('Müşteri seçimi gereklidir'),
  assignedTo: Yup.string().required('Atanan kişi gereklidir'),
  priority: Yup.string().oneOf(['low', 'medium', 'high'], 'Geçersiz öncelik').required('Öncelik gereklidir'),
  dueDate: Yup.date().required('Son tarih gereklidir'),
  checklist: Yup.array().of(
    Yup.object().shape({
      id: Yup.string().required(),
      title: Yup.string().required(),
      completed: Yup.boolean().required()
    })
  )
});

const NewTaskScreen: React.FC<any> = ({ navigation, route }) => {
  const { customers, teamMembers } = route.params || { customers: [], teamMembers: [] };

  const initialValues: TaskFormValues = {
    title: '',
    description: '',
    customerId: '',
    customerName: '',
    assignedTo: '',
    assigneeName: '',
    priority: 'medium',
    dueDate: new Date(),
    checklist: [],
  };

  const handleSubmit = async (values: TaskFormValues, { resetForm, setSubmitting }: any) => {
    try {
      setSubmitting(true);
      await createTask(values);
      navigation.goBack();
      resetForm();
    } catch (error) {
      console.error('Görev oluşturulurken hata:', error);
      setSubmitting(false);
    }
  };

  return (
    <Formik
      initialValues={initialValues}
      validationSchema={validationSchema}
      onSubmit={handleSubmit}
    >
      {(formik) => (
        <ScrollView 
          contentContainerStyle={styles.container}
          keyboardShouldPersistTaps="handled"
          showsVerticalScrollIndicator={false}
        >
          <NewTaskForm formik={formik} />
          <NewTaskCustomerSelect 
            formik={formik} 
            customers={customers} 
          />
          <NewTaskAssigneeSelect 
            formik={formik} 
            teamMembers={teamMembers} 
          />
          <NewTaskPrioritySelect formik={formik} />
          <NewTaskDatePicker formik={formik} />
          <NewTaskChecklist formik={formik} />
          
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
              <Text style={styles.submitButtonText}>Görevi Kaydet</Text>
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
    paddingBottom: Platform.OS === 'ios' ? 100 : 70,
    backgroundColor: lightColors.background,
  },
  submitButton: {
    marginTop: 20,
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
});

export default NewTaskScreen;
