import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  Modal,
  Dimensions,
  FlatList,
  TouchableOpacity,
} from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { Customer } from '../../types/customer';

interface RouteDetailsModalProps {
  visible: boolean;
  routeDetails: {
    customers: Customer[];
    distance: number;
    duration: number;
  } | null;
  onClose: () => void;
  onShowOnMap: () => void;
  onStartNavigation: () => void;
  onCancelRoute: () => void;
}

const MAX_MODAL_HEIGHT = Dimensions.get('window').height * 0.85;

const RouteDetailsModal: React.FC<RouteDetailsModalProps> = ({
  visible,
  routeDetails,
  onClose,
  onShowOnMap,
  onStartNavigation,
  onCancelRoute,
}) => {
  const renderCustomerItem = ({ item, index }: { item: Customer; index: number }) => (
    <View style={styles.customerItem}>
      <View style={styles.orderIndicator}>
        <Text style={styles.orderText}>{index + 1}</Text>
      </View>
      <Text style={styles.customerName}>{item.name}</Text>
      <MaterialCommunityIcons name="map-marker" size={24} color="#00A0E9" />
    </View>
  );

  return (
    <Modal
      animationType="slide"
      transparent={true}
      visible={visible}
      onRequestClose={onClose}
    >
      <View style={styles.modalContainer}>
        <View style={styles.modalContent}>
          <View style={styles.modalHeader}>
            <Text style={styles.headerTitle}>Rota Detayları</Text>
            <TouchableOpacity onPress={onClose}>
              <MaterialCommunityIcons name="close" size={24} color="#1F2937" />
            </TouchableOpacity>
          </View>

          <View style={styles.routeOverview}>
            <View style={styles.routeOverviewItem}>
              <Text style={styles.routeOverviewLabel}>Toplam Mesafe</Text>
              <Text style={styles.routeOverviewValue}>
                {routeDetails?.distance ? `${routeDetails.distance.toFixed(1)} km` : '-'}
              </Text>
            </View>
            <View style={styles.routeOverviewItem}>
              <Text style={styles.routeOverviewLabel}>Tahmini Süre</Text>
              <Text style={styles.routeOverviewValue}>
                {routeDetails?.duration ? `${routeDetails.duration.toFixed(0)} dk` : '-'}
              </Text>
            </View>
          </View>

          <Text style={styles.customerListTitle}>Müşteri Sırası</Text>
          <View style={styles.customerListContainer}>
            <FlatList
              data={routeDetails?.customers || []}
              renderItem={renderCustomerItem}
              keyExtractor={(item) => item.id.toString()}
              ListEmptyComponent={<Text style={styles.emptyText}>Müşteri bulunamadı</Text>}
            />
          </View>

          <View style={styles.buttonStack}>
            <TouchableOpacity style={styles.startNavButton} onPress={onStartNavigation}>
              <MaterialCommunityIcons name="navigation" size={20} color="#FFFFFF" style={{ marginRight: 6 }} />
              <Text style={styles.startNavButtonText}>Harita Uygulamasında Aç (Duraklı Rota)</Text>
            </TouchableOpacity>

            <View style={styles.buttonRow}>
              <TouchableOpacity style={styles.showMapButton} onPress={onShowOnMap}>
                <MaterialCommunityIcons name="map-outline" size={18} color="#00A0E9" style={{ marginRight: 4 }} />
                <Text style={styles.showMapButtonText}>Uygulama İçi Harita</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.cancelButton} onPress={onCancelRoute}>
                <Text style={styles.cancelButtonText}>Vazgeç</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  modalContainer: {
    flex: 1,
    justifyContent: 'flex-end',
    backgroundColor: 'rgba(0,0,0,0.5)',
  },
  modalContent: {
    backgroundColor: '#FFFFFF',
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    maxHeight: MAX_MODAL_HEIGHT,
    padding: 20,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1F2937',
  },
  routeOverview: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 16,
    backgroundColor: '#F3F4F6',
    padding: 14,
    borderRadius: 12,
  },
  routeOverviewItem: {
    alignItems: 'center',
  },
  routeOverviewLabel: {
    color: '#6B7280',
    fontSize: 12,
    marginBottom: 2,
  },
  routeOverviewValue: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1F2937',
  },
  customerListTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#1F2937',
  },
  customerListContainer: {
    maxHeight: 250,
    marginBottom: 16,
  },
  customerItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: '#E5E7EB',
  },
  customerName: {
    flex: 1,
    marginLeft: 12,
    fontSize: 15,
    color: '#1F2937',
    fontWeight: '500',
  },
  orderIndicator: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: '#00A0E9',
    justifyContent: 'center',
    alignItems: 'center',
  },
  orderText: {
    color: '#FFFFFF',
    fontSize: 12,
    fontWeight: 'bold',
  },
  emptyText: {
    color: '#6B7280',
    textAlign: 'center',
    marginVertical: 16,
  },
  buttonStack: {
    marginTop: 8,
    gap: 8,
  },
  startNavButton: {
    height: 46,
    borderRadius: 10,
    backgroundColor: '#00A0E9',
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#00A0E9',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 3,
  },
  startNavButtonText: {
    color: '#FFFFFF',
    fontWeight: 'bold',
    fontSize: 14,
  },
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 8,
  },
  showMapButton: {
    flex: 1,
    height: 42,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#00A0E9',
    backgroundColor: '#FFFFFF',
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  showMapButtonText: {
    color: '#00A0E9',
    fontWeight: 'bold',
    fontSize: 13,
  },
  cancelButton: {
    flex: 1,
    height: 42,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#D1D5DB',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
  },
  cancelButtonText: {
    color: '#4B5563',
    fontWeight: '600',
    fontSize: 13,
  },
});

export default React.memo(RouteDetailsModal);
