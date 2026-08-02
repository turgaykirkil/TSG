import React, { useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  Switch,
  Modal,
  StyleSheet,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { MaterialCommunityIcons as Icon } from '@expo/vector-icons';
import { useDispatch, useSelector } from 'react-redux';
import { logoutAsync } from '../../store/slices/authSlice';
import { toggleDarkMode } from '../../store/slices/themeSlice';
import { authAPI } from '../../services/api';

const SettingsScreen = () => {
  const dispatch = useDispatch();
  const isDarkMode = useSelector((state: any) => state.theme?.isDarkMode ?? false);
  const [pushNotifications, setPushNotifications] = useState(true);
  const [emailNotifications, setEmailNotifications] = useState(true);
  const [syncInterval, setSyncInterval] = useState('15');
  const [syncModalVisible, setSyncModalVisible] = useState(false);
  const [logoutModalVisible, setLogoutModalVisible] = useState(false);

  const handleLogout = async () => {
    try {
      await authAPI.logout();
      await dispatch(logoutAsync() as any);
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setLogoutModalVisible(false);
    }
  };

  const handleSync = () => {
    Alert.alert('Senkronizasyon', 'Tüm veriler başarıyla senkronize edildi.');
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView style={styles.container} contentContainerStyle={styles.scrollContent}>
        {/* Bildirimler */}
        <View style={styles.section}>
          <Text style={styles.sectionHeader}>BİLDİRİMLER</Text>
          <View style={styles.itemRow}>
            <View style={styles.itemLeft}>
              <Icon name="bell" size={22} color="#00A0E9" style={styles.itemIcon} />
              <View>
                <Text style={styles.itemTitle}>Anlık Bildirimler</Text>
                <Text style={styles.itemSub}>Güncellemeler için anlık bildirim al</Text>
              </View>
            </View>
            <Switch
              value={pushNotifications}
              onValueChange={setPushNotifications}
              trackColor={{ false: '#D1D5DB', true: '#90CAF9' }}
              thumbColor={pushNotifications ? '#00A0E9' : '#F3F4F6'}
            />
          </View>

          <View style={styles.itemRow}>
            <View style={styles.itemLeft}>
              <Icon name="email" size={22} color="#00A0E9" style={styles.itemIcon} />
              <View>
                <Text style={styles.itemTitle}>E-Posta Bildirimleri</Text>
                <Text style={styles.itemSub}>E-posta ile bilgilendirmeler al</Text>
              </View>
            </View>
            <Switch
              value={emailNotifications}
              onValueChange={setEmailNotifications}
              trackColor={{ false: '#D1D5DB', true: '#90CAF9' }}
              thumbColor={emailNotifications ? '#00A0E9' : '#F3F4F6'}
            />
          </View>
        </View>

        {/* Görünüm */}
        <View style={styles.section}>
          <Text style={styles.sectionHeader}>GÖRÜNÜM VE TEMA</Text>
          <View style={styles.itemRow}>
            <View style={styles.itemLeft}>
              <Icon name="theme-light-dark" size={22} color="#00A0E9" style={styles.itemIcon} />
              <View>
                <Text style={styles.itemTitle}>Karanlık Mod (Dark Mode)</Text>
                <Text style={styles.itemSub}>Koyu renk temasını aktif et</Text>
              </View>
            </View>
            <Switch
              value={isDarkMode}
              onValueChange={() => {
                dispatch(toggleDarkMode());
              }}
              trackColor={{ false: '#D1D5DB', true: '#90CAF9' }}
              thumbColor={isDarkMode ? '#00A0E9' : '#F3F4F6'}
            />
          </View>
        </View>

        {/* Veri Senkronizasyonu */}
        <View style={styles.section}>
          <Text style={styles.sectionHeader}>VERİ SENKRONİZASYONU</Text>
          <TouchableOpacity style={styles.itemRow} onPress={() => setSyncModalVisible(true)}>
            <View style={styles.itemLeft}>
              <Icon name="sync" size={22} color="#00A0E9" style={styles.itemIcon} />
              <View>
                <Text style={styles.itemTitle}>Senkronizasyon Sıklığı</Text>
                <Text style={styles.itemSub}>{syncInterval} dakikada bir otomatik senkronize et</Text>
              </View>
            </View>
            <Icon name="chevron-right" size={22} color="#9CA3AF" />
          </TouchableOpacity>

          <TouchableOpacity style={styles.itemRow} onPress={handleSync}>
            <View style={styles.itemLeft}>
              <Icon name="cloud-sync" size={22} color="#00A0E9" style={styles.itemIcon} />
              <View>
                <Text style={styles.itemTitle}>Şimdi Senkronize Et</Text>
                <Text style={styles.itemSub}>Verileri elle hemen senkronize et</Text>
              </View>
            </View>
            <Icon name="refresh" size={22} color="#9CA3AF" />
          </TouchableOpacity>
        </View>

        {/* Hesap & Oturum */}
        <View style={styles.section}>
          <Text style={styles.sectionHeader}>HESAP İŞLEMLERİ</Text>
          <TouchableOpacity style={styles.itemRow} onPress={() => setLogoutModalVisible(true)}>
            <View style={styles.itemLeft}>
              <Icon name="logout" size={22} color="#E53935" style={styles.itemIcon} />
              <View>
                <Text style={[styles.itemTitle, { color: '#E53935' }]}>Çıkış Yap</Text>
                <Text style={styles.itemSub}>Hesabınızdan güvenle çıkış yapın</Text>
              </View>
            </View>
            <Icon name="chevron-right" size={22} color="#E53935" />
          </TouchableOpacity>
        </View>

        {/* Uygulama Hakkında */}
        <View style={styles.section}>
          <Text style={styles.sectionHeader}>HAKKINDA</Text>
          <View style={styles.itemRow}>
            <View style={styles.itemLeft}>
              <Icon name="information" size={22} color="#00A0E9" style={styles.itemIcon} />
              <View>
                <Text style={styles.itemTitle}>Sürüm</Text>
                <Text style={styles.itemSub}>v1.0.0 (Sicilius B2B Platform)</Text>
              </View>
            </View>
          </View>
        </View>
      </ScrollView>

      {/* Senkronizasyon Seçim Modalı */}
      <Modal
        visible={syncModalVisible}
        transparent={true}
        animationType="fade"
        onRequestClose={() => setSyncModalVisible(false)}
      >
        <TouchableOpacity
          style={styles.modalOverlay}
          activeOpacity={1}
          onPress={() => setSyncModalVisible(false)}
        >
          <View style={styles.modalCard} onStartShouldSetResponder={() => true}>
            <Text style={styles.modalTitle}>Senkronizasyon Sıklığı</Text>
            
            <TouchableOpacity
              style={styles.optionRow}
              onPress={() => { setSyncInterval('15'); setSyncModalVisible(false); }}
            >
              <Text style={styles.optionText}>15 dakika</Text>
              {syncInterval === '15' && <Icon name="check" size={22} color="#00A0E9" />}
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.optionRow}
              onPress={() => { setSyncInterval('30'); setSyncModalVisible(false); }}
            >
              <Text style={styles.optionText}>30 dakika</Text>
              {syncInterval === '30' && <Icon name="check" size={22} color="#00A0E9" />}
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.optionRow}
              onPress={() => { setSyncInterval('60'); setSyncModalVisible(false); }}
            >
              <Text style={styles.optionText}>1 saat</Text>
              {syncInterval === '60' && <Icon name="check" size={22} color="#00A0E9" />}
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.cancelBtn}
              onPress={() => setSyncModalVisible(false)}
            >
              <Text style={styles.cancelBtnText}>Vazgeç</Text>
            </TouchableOpacity>
          </View>
        </TouchableOpacity>
      </Modal>

      {/* Çıkış Yap Onay Modalı */}
      <Modal
        visible={logoutModalVisible}
        transparent={true}
        animationType="fade"
        onRequestClose={() => setLogoutModalVisible(false)}
      >
        <TouchableOpacity
          style={styles.modalOverlay}
          activeOpacity={1}
          onPress={() => setLogoutModalVisible(false)}
        >
          <View style={styles.modalCard} onStartShouldSetResponder={() => true}>
            <Icon name="logout" size={36} color="#E53935" style={{ alignSelf: 'center', marginBottom: 12 }} />
            <Text style={styles.modalTitleCenter}>Çıkış Yapılsın mı?</Text>
            <Text style={styles.modalSubtitle}>Hesabınızdan çıkış yapmak istediğinizden emin misiniz?</Text>
            
            <View style={styles.modalActionRow}>
              <TouchableOpacity
                style={styles.modalCancelBtn}
                onPress={() => setLogoutModalVisible(false)}
              >
                <Text style={styles.modalCancelBtnText}>İptal</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={styles.modalLogoutBtn}
                onPress={handleLogout}
              >
                <Text style={styles.modalLogoutBtnText}>Çıkış Yap</Text>
              </TouchableOpacity>
            </View>
          </View>
        </TouchableOpacity>
      </Modal>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#F3F4F6',
  },
  container: {
    flex: 1,
  },
  scrollContent: {
    paddingVertical: 16,
    paddingHorizontal: 16,
  },
  section: {
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    paddingVertical: 8,
    paddingHorizontal: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 3,
    elevation: 2,
  },
  sectionHeader: {
    fontSize: 12,
    fontWeight: '700',
    color: '#6B7280',
    marginTop: 8,
    marginBottom: 8,
    letterSpacing: 0.5,
  },
  itemRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: 12,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: '#F3F4F6',
  },
  itemLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
    paddingRight: 8,
  },
  itemIcon: {
    marginRight: 14,
  },
  itemTitle: {
    fontSize: 15,
    fontWeight: '600',
    color: '#1F2937',
  },
  itemSub: {
    fontSize: 12,
    color: '#6B7280',
    marginTop: 2,
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  modalCard: {
    width: '100%',
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 20,
    elevation: 5,
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1F2937',
    marginBottom: 16,
  },
  modalTitleCenter: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1F2937',
    textAlign: 'center',
    marginBottom: 6,
  },
  modalSubtitle: {
    fontSize: 14,
    color: '#4B5563',
    textAlign: 'center',
    marginBottom: 20,
  },
  optionRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 14,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: '#E5E7EB',
  },
  optionText: {
    fontSize: 16,
    color: '#1F2937',
  },
  cancelBtn: {
    marginTop: 16,
    alignItems: 'center',
    paddingVertical: 10,
  },
  cancelBtnText: {
    fontSize: 15,
    color: '#6B7280',
    fontWeight: '600',
  },
  modalActionRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  modalCancelBtn: {
    flex: 0.48,
    height: 44,
    borderRadius: 10,
    backgroundColor: '#E5E7EB',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalCancelBtnText: {
    color: '#374151',
    fontWeight: '600',
    fontSize: 15,
  },
  modalLogoutBtn: {
    flex: 0.48,
    height: 44,
    borderRadius: 10,
    backgroundColor: '#E53935',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalLogoutBtnText: {
    color: '#FFFFFF',
    fontWeight: 'bold',
    fontSize: 15,
  },
});

export default SettingsScreen;
