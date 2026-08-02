import React, { useState } from 'react';
import { View, StyleSheet, TouchableOpacity, Text, Modal, ScrollView } from 'react-native';
import { MaterialCommunityIcons as Icon } from '@expo/vector-icons';
import { FormikProps } from 'formik';
import { TaskFormValues } from '../../types/task';
import { lightColors } from '../../theme';

interface NewTaskCustomerSelectProps {
  formik: FormikProps<TaskFormValues>;
  customers: Array<{ id: string; name: string }>;
}

const NewTaskCustomerSelect: React.FC<NewTaskCustomerSelectProps> = ({ 
  formik, 
  customers 
}) => {
  const [customerMenuVisible, setCustomerMenuVisible] = useState(false);

  const handleCustomerSelect = (customer: { id: string; name: string }) => {
    formik.setFieldValue('customerId', customer.id);
    formik.setFieldValue('customerName', customer.name);
    setCustomerMenuVisible(false);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.label}>Müşteri *</Text>
      <TouchableOpacity 
        style={styles.selectButton} 
        onPress={() => setCustomerMenuVisible(true)}
      >
        <Text style={formik.values.customerName ? styles.selectText : styles.placeholderText}>
          {formik.values.customerName || 'Müşteri Seçiniz'}
        </Text>
        <Icon name="chevron-down" size={20} color={lightColors.subtext} />
      </TouchableOpacity>

      <Modal
        visible={customerMenuVisible}
        transparent
        animationType="fade"
        onRequestClose={() => setCustomerMenuVisible(false)}
      >
        <TouchableOpacity 
          style={styles.modalOverlay} 
          activeOpacity={1} 
          onPress={() => setCustomerMenuVisible(false)}
        >
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Müşteri Seçin</Text>
            <ScrollView style={styles.listScroll}>
              {customers.map((customer) => (
                <TouchableOpacity
                  key={customer.id}
                  style={styles.optionItem}
                  onPress={() => handleCustomerSelect(customer)}
                >
                  <Text style={styles.optionText}>{customer.name}</Text>
                </TouchableOpacity>
              ))}
            </ScrollView>
          </View>
        </TouchableOpacity>
      </Modal>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginTop: 12,
  },
  label: {
    fontSize: 13,
    fontWeight: '600',
    color: lightColors.text,
    marginBottom: 6,
  },
  selectButton: {
    height: 46,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: lightColors.border,
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 12,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  selectText: {
    fontSize: 14,
    color: lightColors.text,
  },
  placeholderText: {
    fontSize: 14,
    color: lightColors.placeholder,
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.4)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  modalContent: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    width: '100%',
    maxWidth: 320,
    maxHeight: 350,
  },
  modalTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: lightColors.text,
    marginBottom: 12,
  },
  listScroll: {
    maxHeight: 260,
  },
  optionItem: {
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: lightColors.border,
  },
  optionText: {
    fontSize: 14,
    color: lightColors.text,
  },
});

export default NewTaskCustomerSelect;
