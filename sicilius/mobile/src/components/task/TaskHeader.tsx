import React from 'react';
import { View, StyleSheet, Text, TouchableOpacity } from 'react-native';
import { MaterialCommunityIcons as Icon } from '@expo/vector-icons';
import { getPriorityColor } from '../../types/task';
import { lightColors } from '../../theme';

interface TaskHeaderProps {
  title: string;
  status: string;
  priority: string;
  onMenuPress: (event: any) => void;
}

export const TaskHeader: React.FC<TaskHeaderProps> = ({
  title,
  status,
  priority,
  onMenuPress,
}) => {
  return (
    <View style={styles.headerCard}>
      <View style={styles.headerContent}>
        <Text style={styles.title}>
          {title}
        </Text>
        <TouchableOpacity onPress={onMenuPress} style={styles.menuButton}>
          <Icon name="dots-vertical" size={24} color={lightColors.text} />
        </TouchableOpacity>
      </View>
      <View style={[styles.statusChip, { backgroundColor: getPriorityColor(priority as any) }]}>
        <Text style={styles.statusChipText}>{status.toUpperCase()}</Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  headerCard: {
    margin: 16,
    padding: 16,
    borderRadius: 12,
    backgroundColor: '#FFFFFF',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 4,
    elevation: 3,
  },
  headerContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  title: {
    flex: 1,
    fontSize: 20,
    fontWeight: 'bold',
    color: lightColors.text,
    marginRight: 16,
  },
  menuButton: {
    padding: 4,
  },
  statusChip: {
    alignSelf: 'flex-start',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  statusChipText: {
    color: '#FFFFFF',
    fontSize: 11,
    fontWeight: 'bold',
  },
});
