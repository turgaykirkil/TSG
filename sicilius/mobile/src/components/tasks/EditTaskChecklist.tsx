import React, { useState } from 'react';
import { View, StyleSheet, Text, TextInput, TouchableOpacity } from 'react-native';
import { MaterialCommunityIcons as Icon } from '@expo/vector-icons';
import { FormikProps } from 'formik';
import { Task } from '../../types/task';
import { lightColors } from '../../theme';

const generateUniqueId = () => {
  return Date.now().toString() + Math.random().toString(36).substr(2, 9);
};

interface EditTaskChecklistProps {
  formik: FormikProps<Task>;
}

const EditTaskChecklist: React.FC<EditTaskChecklistProps> = ({ formik }) => {
  const [newChecklistItem, setNewChecklistItem] = useState('');

  const addChecklistItem = () => {
    if (newChecklistItem.trim()) {
      const newItem = {
        id: generateUniqueId(),
        title: newChecklistItem.trim(),
        completed: false,
      };
      formik.setFieldValue('checklist', [...(formik.values.checklist || []), newItem]);
      setNewChecklistItem('');
    }
  };

  const removeChecklistItem = (id: string) => {
    formik.setFieldValue(
      'checklist', 
      (formik.values.checklist || []).filter(item => item.id !== id)
    );
  };

  const toggleChecklistItem = (id: string) => {
    formik.setFieldValue(
      'checklist', 
      (formik.values.checklist || []).map(item => 
        item.id === id ? { ...item, completed: !item.completed } : item
      )
    );
  };

  const checklist = formik.values.checklist || [];

  return (
    <View style={styles.checklistContainer}>
      <Text style={styles.sectionTitle}>Kontrol Listesi</Text>
      {checklist.length === 0 ? (
        <Text style={styles.emptyText}>Henüz kontrol listesi eklenmemiş</Text>
      ) : (
        checklist.map((item) => (
          <View key={item.id} style={styles.checklistItem}>
            <TouchableOpacity onPress={() => toggleChecklistItem(item.id)} style={styles.checkboxBtn}>
              <Icon 
                name={item.completed ? "checkbox-marked" : "checkbox-blank-outline"} 
                size={22} 
                color={item.completed ? lightColors.primary : lightColors.subtext} 
              />
            </TouchableOpacity>
            <Text style={[styles.checklistTitle, item.completed && styles.completedText]}>
              {item.title}
            </Text>
            <TouchableOpacity onPress={() => removeChecklistItem(item.id)} style={styles.deleteBtn}>
              <Icon name="delete-outline" size={20} color={lightColors.error} />
            </TouchableOpacity>
          </View>
        ))
      )}
      
      <View style={styles.addChecklistContainer}>
        <TextInput
          value={newChecklistItem}
          onChangeText={setNewChecklistItem}
          placeholder="Kontrol listesi maddesi ekle"
          placeholderTextColor={lightColors.placeholder}
          style={styles.addChecklistInput}
          onSubmitEditing={addChecklistItem}
        />
        <TouchableOpacity 
          style={[styles.addBtn, !newChecklistItem.trim() && styles.disabledAddBtn]}
          onPress={addChecklistItem}
          disabled={!newChecklistItem.trim()}
        >
          <Icon name="plus" size={20} color="#FFFFFF" />
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  checklistContainer: {
    marginTop: 16, 
  },
  sectionTitle: {
    fontSize: 15,
    fontWeight: 'bold',
    color: lightColors.text,
    marginBottom: 8,
  },
  checklistItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8, 
    backgroundColor: '#FFFFFF',
    padding: 10,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: lightColors.border,
  },
  checkboxBtn: {
    paddingRight: 8,
  },
  checklistTitle: {
    flex: 1,
    fontSize: 14,
    color: lightColors.text,
  },
  completedText: {
    textDecorationLine: 'line-through',
    color: lightColors.subtext,
  },
  deleteBtn: {
    padding: 4,
  },
  addChecklistContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 8, 
    gap: 8,
  },
  addChecklistInput: {
    flex: 1,
    height: 44,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: lightColors.border,
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 12,
    fontSize: 14,
    color: lightColors.text,
  },
  addBtn: {
    width: 44,
    height: 44,
    borderRadius: 8,
    backgroundColor: lightColors.primary,
    justifyContent: 'center',
    alignItems: 'center',
  },
  disabledAddBtn: {
    opacity: 0.5,
  },
  emptyText: {
    color: lightColors.subtext,
    textAlign: 'center',
    marginVertical: 12, 
    fontSize: 13,
  },
});

export default EditTaskChecklist;
