import React from 'react';
import { View, Text, Modal, TextInput, TouchableOpacity, StyleSheet } from 'react-native';

interface TaskProgressDialogProps {
  visible: boolean;
  onDismiss: () => void;
  onUpdate: () => void;
  progress: string;
  onProgressChange: (value: string) => void;
}

const TaskProgressDialog: React.FC<TaskProgressDialogProps> = ({
  visible,
  onDismiss,
  onUpdate,
  progress,
  onProgressChange,
}) => {
  return (
    <Modal
      visible={visible}
      transparent={true}
      animationType="fade"
      onRequestClose={onDismiss}
    >
      <TouchableOpacity
        style={styles.overlay}
        activeOpacity={1}
        onPress={onDismiss}
      >
        <View style={styles.card} onStartShouldSetResponder={() => true}>
          <Text style={styles.title}>İlerleme Güncelle</Text>
          
          <View style={styles.inputContainer}>
            <Text style={styles.inputLabel}>İlerleme Yüzdesi (%)</Text>
            <TextInput
              style={styles.textInput}
              value={progress}
              onChangeText={onProgressChange}
              keyboardType="numeric"
              maxLength={3}
              placeholder="Örn: 50"
              placeholderTextColor="#9CA3AF"
            />
          </View>

          <View style={styles.actionRow}>
            <TouchableOpacity style={styles.cancelBtn} onPress={onDismiss}>
              <Text style={styles.cancelBtnText}>İptal</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.updateBtn} onPress={onUpdate}>
              <Text style={styles.updateBtnText}>Güncelle</Text>
            </TouchableOpacity>
          </View>
        </View>
      </TouchableOpacity>
    </Modal>
  );
};

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  card: {
    width: '100%',
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 20,
    elevation: 5,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1F2937',
    marginBottom: 16,
  },
  inputContainer: {
    marginBottom: 20,
  },
  inputLabel: {
    fontSize: 13,
    fontWeight: '600',
    color: '#374151',
    marginBottom: 6,
  },
  textInput: {
    height: 46,
    borderWidth: 1,
    borderColor: '#D1D5DB',
    borderRadius: 8,
    paddingHorizontal: 12,
    fontSize: 16,
    color: '#1F2937',
    backgroundColor: '#F9FAFB',
  },
  actionRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  cancelBtn: {
    flex: 0.48,
    height: 44,
    borderRadius: 10,
    backgroundColor: '#E5E7EB',
    justifyContent: 'center',
    alignItems: 'center',
  },
  cancelBtnText: {
    color: '#374151',
    fontWeight: '600',
    fontSize: 15,
  },
  updateBtn: {
    flex: 0.48,
    height: 44,
    borderRadius: 10,
    backgroundColor: '#00A0E9',
    justifyContent: 'center',
    alignItems: 'center',
  },
  updateBtnText: {
    color: '#FFFFFF',
    fontWeight: 'bold',
    fontSize: 15,
  },
});

export default TaskProgressDialog;
