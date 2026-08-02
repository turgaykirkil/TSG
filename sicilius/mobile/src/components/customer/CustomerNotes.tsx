import React, { memo } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Customer } from '../../types/customer';
import { lightColors } from '../../theme';

interface CustomerNotesProps {
  customer: Customer | null;
}

const CustomerNotes = memo<CustomerNotesProps>(({ customer }) => {
  return (
    <View style={styles.container}>
      <Text style={styles.sectionTitle}>Notlar</Text>
      <Text style={styles.notesText}>{customer?.notes || 'Henüz not eklenmedi'}</Text>
    </View>
  );
});

const styles = StyleSheet.create({
  container: {
    paddingVertical: 4,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: lightColors.text,
    marginBottom: 8,
  },
  notesText: {
    fontSize: 14,
    color: lightColors.subtext,
    lineHeight: 20,
  },
});

CustomerNotes.displayName = 'CustomerNotes';

export default CustomerNotes;
