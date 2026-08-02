import React, { memo } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { MaterialCommunityIcons as Icon } from '@expo/vector-icons';
import { Customer } from '../../types/customer';
import { lightColors } from '../../theme';

interface CustomerProfileProps {
  customer: Customer | null;
  onCall: () => void;
  onEmail: () => void;
  onOpenMaps: () => void;
}

const CustomerProfile = memo<CustomerProfileProps>(({
  customer,
  onCall,
  onEmail,
  onOpenMaps
}) => {
  const initials = customer ? customer.name.split(' ').map((n) => n[0]).join('').substring(0, 2).toUpperCase() : 'N/A';

  return (
    <View style={styles.container}>
      <View style={styles.profileHeader}>
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>{initials}</Text>
        </View>
        <View style={styles.profileInfo}>
          <Text style={styles.nameText}>{customer?.name || 'N/A'}</Text>
          <Text style={styles.companyText}>{customer?.company || 'N/A'}</Text>
          <View style={styles.statusContainer}>
            <Icon
              name="circle"
              size={12}
              color={customer?.status === 'active' ? '#10B981' : lightColors.error}
            />
            <Text style={styles.statusText}>
              {customer?.status ? customer.status.charAt(0).toUpperCase() + customer.status.slice(1) : 'N/A'}
            </Text>
          </View>
        </View>
      </View>

      <View style={styles.actionButtons}>
        <TouchableOpacity style={styles.actionButton} onPress={onCall}>
          <Icon name="phone" size={18} color="#FFFFFF" />
          <Text style={styles.actionButtonText}>Ara</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.actionButton} onPress={onEmail}>
          <Icon name="email" size={18} color="#FFFFFF" />
          <Text style={styles.actionButtonText}>E-posta</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.actionButton} onPress={onOpenMaps}>
          <Icon name="map-marker" size={18} color="#FFFFFF" />
          <Text style={styles.actionButtonText}>Harita</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
});

const styles = StyleSheet.create({
  container: {
    paddingVertical: 8,
  },
  profileHeader: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  avatar: {
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: lightColors.primary,
    justifyContent: 'center',
    alignItems: 'center',
  },
  avatarText: {
    color: '#FFFFFF',
    fontSize: 22,
    fontWeight: 'bold',
  },
  profileInfo: {
    flex: 1,
    marginLeft: 16,
  },
  nameText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: lightColors.text,
    marginBottom: 2,
  },
  companyText: {
    fontSize: 14,
    color: lightColors.subtext,
    marginBottom: 4,
  },
  statusContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusText: {
    fontSize: 13,
    marginLeft: 6,
    color: lightColors.text,
  },
  actionButtons: {
    flexDirection: 'row',
    marginTop: 16,
    gap: 8,
  },
  actionButton: {
    flex: 1,
    height: 38,
    borderRadius: 8,
    backgroundColor: lightColors.primary,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: 6,
  },
  actionButtonText: {
    color: '#FFFFFF',
    fontWeight: 'bold',
    fontSize: 13,
  },
});

CustomerProfile.displayName = 'CustomerProfile';

export default CustomerProfile;
