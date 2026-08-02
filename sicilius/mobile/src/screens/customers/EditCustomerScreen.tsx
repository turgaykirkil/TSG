import React, { useState } from 'react';
import { View, StyleSheet, ScrollView, Text, TextInput, TouchableOpacity, ActivityIndicator, Modal } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RouteProp } from '@react-navigation/native';
import { Formik } from 'formik';
import * as Yup from 'yup';
import { CustomerStackParamList } from '../../navigation/types';
import { Customer } from '../../types/customer';
import { updateCustomer } from '../../store/slices/customerSlice';
import { RootState, AppDispatch } from '../../store';
import { lightColors } from '../../theme';

type EditCustomerScreenProps = {
  navigation: NativeStackNavigationProp<CustomerStackParamList, 'EditCustomer'>;
  route: RouteProp<CustomerStackParamList, 'EditCustomer'>;
};

const validationSchema = Yup.object().shape({
  name: Yup.string().required('Müşteri adı zorunludur'),
  company: Yup.string().required('Firma adı zorunludur'),
  email: Yup.string().email('Geçersiz e-posta').required('E-posta zorunludur'),
  phone: Yup.string().required('Telefon zorunludur'),
  address: Yup.object().shape({
    street: Yup.string().required('Sokak/Adres zorunludur'),
    city: Yup.string().required('Şehir zorunludur'),
    state: Yup.string(),
    zipCode: Yup.string(),
    country: Yup.string(),
  }),
  notes: Yup.string(),
});

const EditCustomerScreen: React.FC<EditCustomerScreenProps> = ({ navigation, route }) => {
  const dispatch = useDispatch<AppDispatch>();
  const { customerId } = route.params;
  const { selectedCustomer: customer, loading } = useSelector(
    (state: RootState) => state.customers
  );
  const [discardDialogVisible, setDiscardDialogVisible] = useState(false);

  const handleSubmit = async (values: Partial<Customer>) => {
    try {
      const { id: _, ...restValues } = values;
      await dispatch(updateCustomer({ id: String(customerId), ...restValues }) as any);
      navigation.goBack();
    } catch (error) {
      console.error('Failed to update customer:', error);
    }
  };

  if (!customer || loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={lightColors.primary} />
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <Formik
        initialValues={customer}
        validationSchema={validationSchema}
        onSubmit={handleSubmit}
      >
        {({
          handleChange,
          handleBlur,
          handleSubmit,
          values,
          errors,
          touched,
          dirty,
        }) => (
          <View style={styles.form}>
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Temel Bilgiler</Text>
              <Text style={styles.label}>Müşteri Adı *</Text>
              <TextInput
                style={[styles.input, touched.name && errors.name ? styles.inputError : null]}
                value={values.name}
                onChangeText={handleChange('name')}
                onBlur={handleBlur('name')}
                placeholder="Örn: Ahmet Yılmaz"
                placeholderTextColor={lightColors.placeholder}
              />
              {touched.name && errors.name && (
                <Text style={styles.errorText}>{errors.name}</Text>
              )}

              <Text style={styles.label}>Firma Unvanı *</Text>
              <TextInput
                style={[styles.input, touched.company && errors.company ? styles.inputError : null]}
                value={values.company}
                onChangeText={handleChange('company')}
                onBlur={handleBlur('company')}
                placeholder="Örn: ABC Teknoloji Ltd."
                placeholderTextColor={lightColors.placeholder}
              />
              {touched.company && errors.company && (
                <Text style={styles.errorText}>{errors.company}</Text>
              )}
            </View>

            <View style={styles.divider} />

            <View style={styles.section}>
              <Text style={styles.sectionTitle}>İletişim Bilgileri</Text>
              <Text style={styles.label}>E-posta *</Text>
              <TextInput
                style={[styles.input, touched.email && errors.email ? styles.inputError : null]}
                value={values.email}
                onChangeText={handleChange('email')}
                onBlur={handleBlur('email')}
                keyboardType="email-address"
                autoCapitalize="none"
                placeholder="ornek@firma.com"
                placeholderTextColor={lightColors.placeholder}
              />
              {touched.email && errors.email && (
                <Text style={styles.errorText}>{errors.email}</Text>
              )}

              <Text style={styles.label}>Telefon *</Text>
              <TextInput
                style={[styles.input, touched.phone && errors.phone ? styles.inputError : null]}
                value={values.phone}
                onChangeText={handleChange('phone')}
                onBlur={handleBlur('phone')}
                keyboardType="phone-pad"
                placeholder="05xx xxx xx xx"
                placeholderTextColor={lightColors.placeholder}
              />
              {touched.phone && errors.phone && (
                <Text style={styles.errorText}>{errors.phone}</Text>
              )}
            </View>

            <View style={styles.divider} />

            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Adres Bilgileri</Text>
              <Text style={styles.label}>Sokak/Adres *</Text>
              <TextInput
                style={[styles.input, touched.address?.street && errors.address?.street ? styles.inputError : null]}
                value={values.address?.street}
                onChangeText={handleChange('address.street')}
                onBlur={handleBlur('address.street')}
                placeholder="Mahalle, Cadde, No"
                placeholderTextColor={lightColors.placeholder}
              />
              {touched.address?.street && errors.address?.street && (
                <Text style={styles.errorText}>{errors.address.street}</Text>
              )}

              <Text style={styles.label}>Şehir *</Text>
              <TextInput
                style={[styles.input, touched.address?.city && errors.address?.city ? styles.inputError : null]}
                value={values.address?.city}
                onChangeText={handleChange('address.city')}
                onBlur={handleBlur('address.city')}
                placeholder="İstanbul"
                placeholderTextColor={lightColors.placeholder}
              />
              {touched.address?.city && errors.address?.city && (
                <Text style={styles.errorText}>{errors.address.city}</Text>
              )}
            </View>

            <View style={styles.divider} />

            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Notlar</Text>
              <TextInput
                style={[styles.input, styles.textArea]}
                value={values.notes}
                onChangeText={handleChange('notes')}
                onBlur={handleBlur('notes')}
                multiline
                numberOfLines={4}
                placeholder="Müşteri hakkında özel notlar..."
                placeholderTextColor={lightColors.placeholder}
              />
            </View>

            <View style={styles.buttonContainer}>
              <TouchableOpacity style={styles.saveButton} onPress={() => handleSubmit()}>
                <Text style={styles.saveButtonText}>Kaydet</Text>
              </TouchableOpacity>
              <TouchableOpacity 
                style={styles.cancelButton} 
                onPress={() => {
                  if (dirty) {
                    setDiscardDialogVisible(true);
                  } else {
                    navigation.goBack();
                  }
                }}
              >
                <Text style={styles.cancelButtonText}>Vazgeç</Text>
              </TouchableOpacity>
            </View>

            <Modal
              visible={discardDialogVisible}
              transparent
              animationType="fade"
              onRequestClose={() => setDiscardDialogVisible(false)}
            >
              <View style={styles.modalOverlay}>
                <View style={styles.dialogContent}>
                  <Text style={styles.dialogTitle}>Değişiklikleri İptal Et?</Text>
                  <Text style={styles.dialogText}>
                    Kaydedilmemiş değişiklikleriniz var. Çıkmak istediğinizden emin misiniz?
                  </Text>
                  <View style={styles.dialogActions}>
                    <TouchableOpacity 
                      style={styles.dialogKeepBtn} 
                      onPress={() => setDiscardDialogVisible(false)}
                    >
                      <Text style={styles.dialogKeepText}>Düzenlemeye Devam Et</Text>
                    </TouchableOpacity>
                    <TouchableOpacity
                      style={styles.dialogDiscardBtn}
                      onPress={() => {
                        setDiscardDialogVisible(false);
                        navigation.goBack();
                      }}
                    >
                      <Text style={styles.dialogDiscardText}>Vazgeç</Text>
                    </TouchableOpacity>
                  </View>
                </View>
              </View>
            </Modal>
          </View>
        )}
      </Formik>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: lightColors.background,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: lightColors.background,
  },
  form: {
    padding: 16,
  },
  section: {
    marginBottom: 8,
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
    marginBottom: 10,
  },
  inputError: {
    borderColor: lightColors.error,
  },
  textArea: {
    height: 90,
    textAlignVertical: 'top',
    paddingTop: 10,
  },
  divider: {
    height: 1,
    backgroundColor: lightColors.border,
    marginVertical: 16,
  },
  buttonContainer: {
    flexDirection: 'row',
    marginTop: 16,
    gap: 12,
  },
  saveButton: {
    flex: 1,
    height: 44,
    borderRadius: 8,
    backgroundColor: lightColors.primary,
    justifyContent: 'center',
    alignItems: 'center',
  },
  saveButtonText: {
    color: '#FFFFFF',
    fontWeight: 'bold',
    fontSize: 15,
  },
  cancelButton: {
    flex: 1,
    height: 44,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: lightColors.error,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
  },
  cancelButtonText: {
    color: lightColors.error,
    fontWeight: '600',
    fontSize: 15,
  },
  errorText: {
    color: lightColors.error,
    fontSize: 12,
    marginTop: -6,
    marginBottom: 8,
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
  dialogKeepBtn: {
    paddingHorizontal: 12,
    paddingVertical: 8,
  },
  dialogKeepText: {
    color: lightColors.primary,
    fontWeight: '600',
  },
  dialogDiscardBtn: {
    backgroundColor: lightColors.error,
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 6,
  },
  dialogDiscardText: {
    color: '#FFFFFF',
    fontWeight: 'bold',
  },
});

export default EditCustomerScreen;
