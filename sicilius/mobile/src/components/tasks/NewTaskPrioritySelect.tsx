import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { FormikProps } from 'formik';
import { TaskFormValues } from '../../types/task';

interface NewTaskPrioritySelectProps {
  formik: FormikProps<TaskFormValues>;
}

const NewTaskPrioritySelect: React.FC<NewTaskPrioritySelectProps> = ({ formik }) => {
  const handlePrioritySelect = (priority: 'low' | 'medium' | 'high') => {
    formik.setFieldValue('priority', priority);
  };

  const options: Array<{ value: 'low' | 'medium' | 'high'; label: string; activeColor: string }> = [
    { value: 'low', label: 'Düşük', activeColor: '#10B981' },
    { value: 'medium', label: 'Orta', activeColor: '#F59E0B' },
    { value: 'high', label: 'Yüksek', activeColor: '#EF4444' },
  ];

  return (
    <View style={styles.container}>
      <Text style={styles.label}>Öncelik Seç</Text>
      <View style={styles.priorityContainer}>
        {options.map((opt) => {
          const isSelected = formik.values.priority === opt.value;
          return (
            <TouchableOpacity
              key={opt.value}
              onPress={() => handlePrioritySelect(opt.value)}
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
  priorityContainer: {
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
    fontSize: 14,
    fontWeight: '600',
  },
});

export default NewTaskPrioritySelect;
