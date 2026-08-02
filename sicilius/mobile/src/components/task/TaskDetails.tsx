import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { formatDate } from '../../types/task';

interface TaskDetailsProps {
  description: string;
  priority: string;
  dueDate: string;
  customerName: string;
  onCustomerPress: () => void;
}

export const TaskDetails: React.FC<TaskDetailsProps> = ({
  description,
  priority,
  dueDate,
  customerName,
  onCustomerPress,
}) => {
  return (
    <View style={styles.contentCard}>
      <Text style={styles.sectionTitle}>Detaylar</Text>
      <Text style={styles.description}>{description}</Text>

      <View style={styles.divider} />

      <View style={styles.detailsGrid}>
        <View style={styles.detailItem}>
          <Text style={styles.label}>Öncelik</Text>
          <View style={styles.priorityChip}>
            <Text style={styles.priorityChipText}>{priority}</Text>
          </View>
        </View>

        <View style={styles.detailItem}>
          <Text style={styles.label}>Bitiş Tarihi</Text>
          <Text style={styles.valueText}>{formatDate(dueDate)}</Text>
        </View>

        <TouchableOpacity style={styles.detailItem} onPress={onCustomerPress}>
          <Text style={styles.label}>Müşteri</Text>
          <Text style={styles.linkText}>{customerName}</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  contentCard: {
    marginHorizontal: 16,
    marginVertical: 8,
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.08,
    shadowRadius: 3,
    elevation: 2,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1F2937',
    marginBottom: 8,
  },
  description: {
    fontSize: 15,
    color: '#4B5563',
    lineHeight: 22,
    marginBottom: 12,
  },
  divider: {
    height: StyleSheet.hairlineWidth,
    backgroundColor: '#E5E7EB',
    marginVertical: 12,
  },
  detailsGrid: {
    gap: 12,
  },
  detailItem: {
    gap: 4,
  },
  label: {
    fontSize: 12,
    fontWeight: '600',
    color: '#6B7280',
  },
  valueText: {
    fontSize: 15,
    color: '#1F2937',
  },
  priorityChip: {
    alignSelf: 'flex-start',
    backgroundColor: '#E0F2FE',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#0284C7',
  },
  priorityChipText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#0369A1',
  },
  linkText: {
    fontSize: 15,
    fontWeight: '600',
    color: '#00A0E9',
  },
});
