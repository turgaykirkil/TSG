import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import DateTimePicker from '@react-native-community/datetimepicker';
import { FormikProps } from 'formik';
import { TaskFormValues } from '../../types/task';
import { formatDate } from '../../utils/display';
import { MaterialCommunityIcons as Icon } from '@expo/vector-icons';

interface NewTaskDatePickerProps {
  formik: FormikProps<TaskFormValues>;
}

const NewTaskDatePicker: React.FC<NewTaskDatePickerProps> = ({ formik }) => {
  const [showDatePicker, setShowDatePicker] = useState(false);

  const handleDateChange = (event: any, selectedDate?: Date) => {
    setShowDatePicker(false);
    if (selectedDate) {
      formik.setFieldValue('dueDate', selectedDate);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.label}>Son Tarih</Text>
      <TouchableOpacity
        style={styles.dateButton}
        onPress={() => setShowDatePicker(true)}
      >
        <Icon name="calendar" size={20} color="#00A0E9" style={{ marginRight: 8 }} />
        <Text style={styles.dateText}>{formatDate(formik.values.dueDate)}</Text>
      </TouchableOpacity>

      {showDatePicker && (
        <DateTimePicker
          testID="dateTimePicker"
          value={formik.values.dueDate}
          mode="date"
          is24Hour={true}
          onChange={handleDateChange}
          minimumDate={new Date()}
        />
      )}
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
    marginBottom: 6,
  },
  dateButton: {
    flexDirection: 'row',
    alignItems: 'center',
    height: 46,
    borderWidth: 1,
    borderColor: '#D1D5DB',
    borderRadius: 8,
    paddingHorizontal: 12,
    backgroundColor: '#FFFFFF',
  },
  dateText: {
    fontSize: 15,
    color: '#1F2937',
  },
});

export default NewTaskDatePicker;
