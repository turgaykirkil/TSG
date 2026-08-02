import React, { useState } from 'react';
import { View, StyleSheet, ScrollView, Text, TouchableOpacity, ActivityIndicator, Modal } from 'react-native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RouteProp } from '@react-navigation/native';
import { CustomerStackParamList } from '../../navigation/types';
import { useCustomerDetail } from '../../hooks/useCustomerDetail';
import { useCustomerActions } from '../../hooks/useCustomerActions';
import CustomerProfile from '../../components/customer/CustomerProfile';
import CustomerContact from '../../components/customer/CustomerContact';
import CustomerOverview from '../../components/customer/CustomerOverview';
import CustomerTasks from '../../components/customer/CustomerTasks';
import CustomerNotes from '../../components/customer/CustomerNotes';
import { lightColors } from '../../theme';

interface CustomerDetailScreenProps {
  navigation: NativeStackNavigationProp<CustomerStackParamList, 'CustomerDetail'>;
  route: RouteProp<CustomerStackParamList, 'CustomerDetail'>;
}

const CustomerDetailScreen: React.FC<CustomerDetailScreenProps> = ({ navigation, route }) => {
  const [deleteDialogVisible, setDeleteDialogVisible] = useState(false);

  const { customer, loading, error } = useCustomerDetail({
    customerId: route.params?.customerId,
  });

  const { handleCall, handleEmail, handleOpenMaps } = useCustomerActions(customer);

  if (error) {
    return (
      <View style={[styles.container, styles.centerContent]}>
        <Text style={styles.errorText}>{error}</Text>
        <TouchableOpacity style={styles.errorButton} onPress={() => navigation.goBack()}>
          <Text style={styles.errorButtonText}>Geri Dön</Text>
        </TouchableOpacity>
      </View>
    );
  }

  if (loading) {
    return (
      <View style={[styles.container, styles.centerContent]}>
        <ActivityIndicator size="large" color={lightColors.primary} />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <ScrollView 
        contentContainerStyle={styles.contentContainer}
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.card}>
          <CustomerProfile
            customer={customer}
            onCall={handleCall}
            onEmail={handleEmail}
            onOpenMaps={handleOpenMaps}
          />
        </View>

        <View style={styles.card}>
          <CustomerContact customer={customer} />
        </View>

        <View style={styles.card}>
          <CustomerOverview customer={customer} />
        </View>

        <View style={styles.card}>
          <CustomerTasks
            customer={customer}
            onSeeAll={() => navigation.navigate('Tasks' as any, { customerId: customer?.id } as any)}
          />
        </View>

        <View style={[styles.card, styles.lastCard]}>
          <CustomerNotes customer={customer} />
        </View>
      </ScrollView>

      <Modal
        visible={deleteDialogVisible}
        transparent
        animationType="fade"
        onRequestClose={() => setDeleteDialogVisible(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.dialogContent}>
            <Text style={styles.dialogTitle}>Müşteriyi Sil</Text>
            <Text style={styles.dialogText}>Bu müşteriyi silmek istediğinizden emin misiniz?</Text>
            <View style={styles.dialogActions}>
              <TouchableOpacity style={styles.dialogCancelBtn} onPress={() => setDeleteDialogVisible(false)}>
                <Text style={styles.dialogCancelText}>İptal</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.dialogDeleteBtn} onPress={() => setDeleteDialogVisible(false)}>
                <Text style={styles.dialogDeleteText}>Sil</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: lightColors.background,
  },
  centerContent: {
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  contentContainer: {
    padding: 16,
    paddingBottom: 32,
  },
  card: {
    backgroundColor: '#FFFFFF',
    marginBottom: 16,
    borderRadius: 12,
    padding: 14,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 4,
    elevation: 3,
  },
  lastCard: {
    marginBottom: 16,
  },
  errorText: {
    fontSize: 15,
    color: lightColors.error,
    textAlign: 'center',
    marginBottom: 16,
  },
  errorButton: {
    backgroundColor: lightColors.primary,
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
  },
  errorButtonText: {
    color: '#FFFFFF',
    fontWeight: 'bold',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  dialogContent: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 20,
    width: '100%',
    maxWidth: 340,
  },
  dialogTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: lightColors.text,
    marginBottom: 8,
  },
  dialogText: {
    fontSize: 14,
    color: lightColors.subtext,
    marginBottom: 20,
  },
  dialogActions: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    gap: 12,
  },
  dialogCancelBtn: {
    paddingHorizontal: 16,
    paddingVertical: 8,
  },
  dialogCancelText: {
    color: lightColors.subtext,
    fontWeight: '600',
  },
  dialogDeleteBtn: {
    backgroundColor: lightColors.error,
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 6,
  },
  dialogDeleteText: {
    color: '#FFFFFF',
    fontWeight: 'bold',
  },
});

export default CustomerDetailScreen;
