import React from 'react';
import { View, Text, TextInput, StyleSheet } from 'react-native';
import { FormikProps } from 'formik';
import { TaskFormValues } from '../../types/task';

interface NewTaskFormProps {
  formik: FormikProps<TaskFormValues>;
}

const NewTaskForm: React.FC<NewTaskFormProps> = ({ formik }) => {
  const isTitleError = formik.touched.title && !!formik.errors.title;
  const isDescError = formik.touched.description && !!formik.errors.description;

  return (
    <View style={styles.container}>
      <View style={styles.inputGroup}>
        <Text style={styles.label}>Görev Başlığı</Text>
        <TextInput
          style={[styles.input, isTitleError ? styles.inputError : null]}
          value={formik.values.title}
          onChangeText={formik.handleChange('title')}
          onBlur={formik.handleBlur('title')}
          placeholder="Örn: Müşteri Ziyareti"
          placeholderTextColor="#9CA3AF"
        />
        {isTitleError ? (
          <Text style={styles.errorText}>{formik.errors.title}</Text>
        ) : null}
      </View>

      <View style={styles.inputGroup}>
        <Text style={styles.label}>Açıklama</Text>
        <TextInput
          style={[styles.input, styles.textArea, isDescError ? styles.inputError : null]}
          value={formik.values.description}
          onChangeText={formik.handleChange('description')}
          onBlur={formik.handleBlur('description')}
          placeholder="Görev detaylarını yazınız..."
          placeholderTextColor="#9CA3AF"
          multiline
          numberOfLines={4}
          textAlignVertical="top"
        />
        {isDescError ? (
          <Text style={styles.errorText}>{formik.errors.description}</Text>
        ) : null}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    gap: 16,
  },
  inputGroup: {
    gap: 6,
  },
  label: {
    fontSize: 13,
    fontWeight: '600',
    color: '#374151',
  },
  input: {
    height: 46,
    borderWidth: 1,
    borderColor: '#D1D5DB',
    borderRadius: 8,
    paddingHorizontal: 12,
    fontSize: 15,
    color: '#1F2937',
    backgroundColor: '#FFFFFF',
  },
  textArea: {
    height: 100,
    paddingTop: 10,
  },
  inputError: {
    borderColor: '#EF4444',
  },
  errorText: {
    fontSize: 12,
    color: '#EF4444',
  },
});

export default NewTaskForm;
