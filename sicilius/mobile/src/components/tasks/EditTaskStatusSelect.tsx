import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { FormikProps } from 'formik';
import { Task } from '../../types/task';

interface EditTaskStatusSelectProps {
  formik: FormikProps<Task>;
}

const EditTaskStatusSelect: React.FC<EditTaskStatusSelectProps> = ({ formik }) => {
  const handleStatusSelect = (status: 'pending' | 'in_progress' | 'completed' | 'todo') => {
    formik.setFieldValue('status', status);
  };

  const options: Array<{ value: 'pending' | 'in_progress' | 'completed'; label: string; activeColor: string }> = [
    { value: 'pending', label: 'Yapılacak', activeColor: '#F59E0B' },
    { value: 'in_progress', label: 'Devam Ediyor', activeColor: '#00A0E9' },
    { value: 'completed', label: 'Tamamlandı', activeColor: '#10B981' },
  ];

  return (
    <View style={styles.container}>
      <Text style={styles.label}>Durum Seç</Text>
      <View style={styles.statusContainer}>
        {options.map((opt) => {
          const isSelected = formik.values.status === opt.value || (opt.value === 'pending' && formik.values.status === 'todo');
          return (
            <TouchableOpacity
              key={opt.value}
              onPress={() => handleStatusSelect(opt.value)}
              style={[
                styles.chip,
                isSelected
                  ? { backgroundColor: opt.activeColor, borderColor: opt.activeColor }
                  : { backgroundColor: '#FFFFFF', borderColor: '#D1D5DB' },
              ]}
            >
              <Text
                style={[
                  styles.chipText,
                  isSelected ? { color: '#FFFFFF' } : { color: opt.activeColor },
                ]}
              >
                {opt.label}
              </Text>
            </TouchableOpacity>
          );
        })}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginTop: 16,
  },
  label: {
    fontSize: 13,
    fontWeight: '600',
    color: '#374151',
    marginBottom: 8,
  },
  statusContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 8,
  },
  chip: {
    flex: 1,
    height: 42,
    borderRadius: 8,
    borderWidth: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  chipText: {
    fontSize: 13,
    fontWeight: '600',
  },
});

export default EditTaskStatusSelect;
