import React, { useState } from 'react';
import {
  View,
  ScrollView,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  Alert,
  Text,
  TextInput,
  TouchableOpacity,
  ActivityIndicator,
} from 'react-native';
import { MaterialCommunityIcons as Icon } from '@expo/vector-icons';
import { useDispatch } from 'react-redux';
import { useNavigation } from '@react-navigation/native';
import { CustomerStackNavigationProp } from '../../navigation/types';
import { createCustomer } from '../../store/slices/customerSlice';
import * as LocationModule from 'expo-location';
import { lightColors } from '../../theme';

interface CustomerForm {
  name: string;
  company: string;
  email: string;
  phone: string;
  address: {
    street: string;
    city: string;
    state: string;
    zipCode: string;
    country: string;
    coordinates: {
      lat: number;
      lng: number;
    };
  };
}

const initialFormState: CustomerForm = {
  name: '',
  company: '',
  email: '',
  phone: '',
  address: {
    street: '',
    city: '',
    state: '',
    zipCode: '',
    country: '',
    coordinates: {
      lat: 0,
      lng: 0,
    },
  },
};

const NewCustomerScreen = () => {
  const dispatch = useDispatch();
  const navigation = useNavigation<CustomerStackNavigationProp>();
  const [form, setForm] = useState<CustomerForm>(initialFormState);
  const [errors, setErrors] = useState<Partial<CustomerForm>>({});
  const [loading, setLoading] = useState(false);

  const validateForm = () => {
    const newErrors: Partial<CustomerForm> = {};

    if (!form.name.trim()) {
      newErrors.name = 'İsim gerekli';
    }
    if (!form.company.trim()) {
      newErrors.company = 'Şirket adı gerekli';
    }
    if (!form.email.trim()) {
      newErrors.email = 'E-posta gerekli';
    } else if (!/\S+@\S+\.\S+/.test(form.email)) {
      newErrors.email = 'Geçerli bir e-posta adresi girin';
    }
    if (!form.phone.trim()) {
      newErrors.phone = 'Telefon numarası gerekli';
    }
    if (!form.address.street.trim()) {
      newErrors.address = { ...newErrors.address, street: 'Adres gerekli' } as any;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const getCurrentLocation = async () => {
    try {
      const { status } = await LocationModule.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        Alert.alert('Hata', 'Konum izni reddedildi');
        return;
      }
      const pos = await LocationModule.getCurrentPositionAsync({});
      setForm(prev => ({
        ...prev,
        address: {
          ...prev.address,
          coordinates: {
            lat: pos.coords.latitude,
            lng: pos.coords.longitude,
          },
        },
      }));
      Alert.alert('Başarılı', 'Konum koordinatları alındı');
    } catch (e: any) {
      Alert.alert('Hata', 'Konum alınamadı: ' + e.message);
    }
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;

    setLoading(true);
    try {
      await dispatch(createCustomer(form) as any);
      navigation.goBack();
    } catch (error) {
      Alert.alert('Hata', 'Müşteri eklenirken bir hata oluştu');
    } finally {
      setLoading(false);
    }
  };

  const updateForm = (field: string, value: string) => {
    if (field.includes('.')) {
      const [parent, child] = field.split('.');
      setForm(prev => ({
        ...prev,
        [parent]: {
          ...((prev as any)[parent] || {}),
          [child]: value,
        },
      }));
    } else {
      setForm(prev => ({ ...prev, [field]: value }));
    }
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={styles.container}
    >
      <ScrollView style={styles.scrollView} contentContainerStyle={styles.contentContainer}>
        <View style={styles.surface}>
          <Text style={styles.sectionTitle}>Temel Bilgiler</Text>

          <Text style={styles.label}>İsim Soyisim *</Text>
          <TextInput
            style={[styles.input, errors.name ? styles.inputError : null]}
            value={form.name}
            onChangeText={(value) => updateForm('name', value)}
            placeholder="Ahmet Yılmaz"
            placeholderTextColor={lightColors.placeholder}
          />
          {errors.name && <Text style={styles.errorText}>{errors.name}</Text>}

          <Text style={styles.label}>Şirket *</Text>
          <TextInput
            style={[styles.input, errors.company ? styles.inputError : null]}
            value={form.company}
            onChangeText={(value) => updateForm('company', value)}
            placeholder="ABC Teknoloji"
            placeholderTextColor={lightColors.placeholder}
          />
          {errors.company && <Text style={styles.errorText}>{errors.company}</Text>}

          <Text style={styles.label}>E-posta *</Text>
          <TextInput
            style={[styles.input, errors.email ? styles.inputError : null]}
            value={form.email}
            onChangeText={(value) => updateForm('email', value)}
            keyboardType="email-address"
            autoCapitalize="none"
            placeholder="ornek@firma.com"
            placeholderTextColor={lightColors.placeholder}
          />
          {errors.email && <Text style={styles.errorText}>{errors.email}</Text>}

          <Text style={styles.label}>Telefon *</Text>
          <TextInput
            style={[styles.input, errors.phone ? styles.inputError : null]}
            value={form.phone}
            onChangeText={(value) => updateForm('phone', value)}
            keyboardType="phone-pad"
            placeholder="05xx xxx xx xx"
            placeholderTextColor={lightColors.placeholder}
          />
          {errors.phone && <Text style={styles.errorText}>{errors.phone}</Text>}
        </View>

        <View style={styles.surface}>
          <View style={styles.addressHeader}>
            <Text style={styles.sectionTitle}>Adres Bilgileri</Text>
            <TouchableOpacity style={styles.gpsButton} onPress={getCurrentLocation}>
              <Icon name="crosshairs-gps" size={16} color="#FFFFFF" />
              <Text style={styles.gpsText}>GPS Konum Al</Text>
            </TouchableOpacity>
          </View>

          <Text style={styles.label}>Sokak/Cadde *</Text>
          <TextInput
            style={[styles.input, errors.address?.street ? styles.inputError : null]}
            value={form.address.street}
            onChangeText={(value) => updateForm('address.street', value)}
            placeholder="Mahalle, Cadde, No"
            placeholderTextColor={lightColors.placeholder}
          />
          {errors.address?.street && <Text style={styles.errorText}>{errors.address.street}</Text>}

          <View style={styles.row}>
            <View style={styles.flex1}>
              <Text style={styles.label}>Şehir</Text>
              <TextInput
                style={styles.input}
                value={form.address.city}
                onChangeText={(value) => updateForm('address.city', value)}
                placeholder="İstanbul"
                placeholderTextColor={lightColors.placeholder}
              />
            </View>
            <View style={styles.flex1}>
              <Text style={styles.label}>İlçe</Text>
              <TextInput
                style={styles.input}
                value={form.address.state}
                onChangeText={(value) => updateForm('address.state', value)}
                placeholder="Kadıköy"
                placeholderTextColor={lightColors.placeholder}
              />
            </View>
          </View>

          <View style={styles.row}>
            <View style={styles.flex1}>
              <Text style={styles.label}>Posta Kodu</Text>
              <TextInput
                style={styles.input}
                value={form.address.zipCode}
                onChangeText={(value) => updateForm('address.zipCode', value)}
                keyboardType="number-pad"
                placeholder="34000"
                placeholderTextColor={lightColors.placeholder}
              />
            </View>
            <View style={styles.flex1}>
              <Text style={styles.label}>Ülke</Text>
              <TextInput
                style={styles.input}
                value={form.address.country}
                onChangeText={(value) => updateForm('address.country', value)}
                placeholder="Türkiye"
                placeholderTextColor={lightColors.placeholder}
              />
            </View>
          </View>
        </View>

        <View style={styles.buttonContainer}>
          <TouchableOpacity 
            style={[styles.submitButton, loading && styles.disabledBtn]} 
            onPress={handleSubmit}
            disabled={loading}
          >
            {loading ? (
              <ActivityIndicator color="#FFFFFF" size="small" />
            ) : (
              <Text style={styles.submitButtonText}>Müşteri Ekle</Text>
            )}
          </TouchableOpacity>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: lightColors.background,
  },
  scrollView: {
    flex: 1,
  },
  contentContainer: {
    padding: 16,
  },
  surface: {
    backgroundColor: '#FFFFFF',
    marginBottom: 16,
    padding: 16,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 4,
    elevation: 3,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: lightColors.text,
    marginBottom: 12,
  },
  label: {
    fontSize: 13,
    fontWeight: '600',
    color: lightColors.text,
    marginBottom: 6,
  },
  input: {
    height: 46,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: lightColors.border,
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 12,
    fontSize: 14,
    color: lightColors.text,
    marginBottom: 8,
  },
  inputError: {
    borderColor: lightColors.error,
  },
  errorText: {
    color: lightColors.error,
    fontSize: 12,
    marginTop: -4,
    marginBottom: 8,
  },
  addressHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  gpsButton: {
    backgroundColor: lightColors.primary,
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 6,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  gpsText: {
    color: '#FFFFFF',
    fontSize: 12,
    fontWeight: '600',
  },
  row: {
    flexDirection: 'row',
    gap: 12,
  },
  flex1: {
    flex: 1,
  },
  buttonContainer: {
    paddingVertical: 8,
    paddingBottom: 32,
  },
  submitButton: {
    height: 48,
    borderRadius: 8,
    backgroundColor: lightColors.primary,
    justifyContent: 'center',
    alignItems: 'center',
  },
  disabledBtn: {
    opacity: 0.6,
  },
  submitButtonText: {
    color: '#FFFFFF',
    fontWeight: 'bold',
    fontSize: 15,
  },
});

export default NewCustomerScreen;
