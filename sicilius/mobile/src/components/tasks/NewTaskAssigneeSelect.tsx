import React, { useState } from 'react';
import { View, StyleSheet, TouchableOpacity, Text, Modal, ScrollView } from 'react-native';
import { MaterialCommunityIcons as Icon } from '@expo/vector-icons';
import { FormikProps } from 'formik';
import { TaskFormValues } from '../../types/task';
import { lightColors } from '../../theme';

interface NewTaskAssigneeSelectProps {
  formik: FormikProps<TaskFormValues>;
  teamMembers: Array<{ id: string; name: string }>;
}

const NewTaskAssigneeSelect: React.FC<NewTaskAssigneeSelectProps> = ({ 
  formik, 
  teamMembers 
}) => {
  const [assigneeMenuVisible, setAssigneeMenuVisible] = useState(false);

  const handleAssigneeSelect = (member: { id: string; name: string }) => {
    formik.setFieldValue('assignedTo', member.id);
    formik.setFieldValue('assigneeName', member.name);
    setAssigneeMenuVisible(false);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.label}>Atanan Kişi *</Text>
      <TouchableOpacity 
        style={styles.selectButton} 
        onPress={() => setAssigneeMenuVisible(true)}
      >
        <Text style={formik.values.assigneeName ? styles.selectText : styles.placeholderText}>
          {formik.values.assigneeName || 'Atanan Kişi Seçiniz'}
        </Text>
        <Icon name="chevron-down" size={20} color={lightColors.subtext} />
      </TouchableOpacity>

      <Modal
        visible={assigneeMenuVisible}
        transparent
        animationType="fade"
        onRequestClose={() => setAssigneeMenuVisible(false)}
      >
        <TouchableOpacity 
          style={styles.modalOverlay} 
          activeOpacity={1} 
          onPress={() => setAssigneeMenuVisible(false)}
        >
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Atanan Kişi Seçin</Text>
            <ScrollView style={styles.listScroll}>
              {teamMembers.map((member) => (
                <TouchableOpacity
                  key={member.id}
                  style={styles.optionItem}
                  onPress={() => handleAssigneeSelect(member)}
                >
                  <Text style={styles.optionText}>{member.name}</Text>
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

export default NewTaskAssigneeSelect;
