import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ActivityIndicator,
  StyleSheet,
  Dimensions,
  Alert,
} from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import * as Yup from 'yup';
import { Formik } from 'formik';
import { authAPI } from '../../services/api';

const { height } = Dimensions.get('window');

const validationSchema = Yup.object().shape({
  firstName: Yup.string().required('Ad alanı zorunludur'),
  lastName: Yup.string().required('Soyad alanı zorunludur'),
  email: Yup.string().email('Geçersiz e-posta adresi').required('E-posta adresi zorunludur'),
  password: Yup.string()
    .min(8, 'Şifre en az 8 karakter olmalıdır')
    .required('Şifre zorunludur'),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref('password')], 'Şifreler eşleşmiyor')
    .required('Şifre tekrarı zorunludur'),
});

interface RegisterFormProps {
  onRegistrationSuccess?: () => void;
}

const RegisterForm: React.FC<RegisterFormProps> = ({ onRegistrationSuccess }) => {
  const navigation = useNavigation();
  const [loading, setLoading] = useState(false);
  const [secureTextEntry, setSecureTextEntry] = useState(true);
  const [secureConfirmTextEntry, setSecureConfirmTextEntry] = useState(true);

  const handleRegister = async (values: any, { setSubmitting }: any) => {
    try {
      setLoading(true);
      console.log('Register submit values:', values);
      const fullName = `${values.firstName} ${values.lastName}`.trim();
      const result = await authAPI.register({
        email: values.email,
        password: values.password,
        full_name: fullName,
      });
      console.log('Register successful:', result);
      Alert.alert(
        'Başarılı',
        'Hesabınız başarıyla oluşturuldu! Şimdi giriş yapabilirsiniz.',
        [
          {
            text: 'Giriş Yap',
            onPress: () => {
              if (onRegistrationSuccess) {
                onRegistrationSuccess();
              } else {
                (navigation as any).navigate('Login');
              }
            },
          },
        ]
      );
    } catch (error: any) {
      let errMsg =
        error?.data?.detail ||
        error?.response?.data?.detail ||
        error?.message ||
        'Kayıt işlemi gerçekleştirilemedi.';

      if (typeof errMsg === 'string' && errMsg.includes('already exists')) {
        Alert.alert(
          'Zaten Kayıtlısınız',
          'Bu e-posta adresi ile açılmış bir hesabınız bulunuyor. Doğrudan giriş yapabilirsiniz.',
          [
            {
              text: 'Giriş Yap',
              onPress: () => {
                if (onRegistrationSuccess) {
                  onRegistrationSuccess();
                } else {
                  (navigation as any).navigate('Login');
                }
              },
            },
            { text: 'Kapat', style: 'cancel' },
          ]
        );
      } else {
        console.warn('Registration exception:', error);
        Alert.alert('Kayıt Uyarısı', typeof errMsg === 'string' ? errMsg : JSON.stringify(errMsg));
      }
    } finally {
      setLoading(false);
      setSubmitting(false);
    }
  };

  return (
    <View style={styles.formContainer}>
      <Formik
        initialValues={{
          firstName: '',
          lastName: '',
          email: '',
          password: '',
          confirmPassword: '',
        }}
        validationSchema={validationSchema}
        onSubmit={handleRegister}
      >
        {({
          handleChange,
          handleBlur,
          handleSubmit,
          values,
          errors,
          touched,
        }) => (
          <View style={styles.fieldsWrapper}>
            {/* Ad & Soyad Row */}
            <View style={styles.row}>
              <View style={styles.halfInputContainer}>
                <Text style={styles.label}>Ad</Text>
                <View style={[styles.inputWrapper, touched.firstName && errors.firstName ? styles.inputError : null]}>
                  <MaterialCommunityIcons name="account" size={20} color="#666" style={styles.inputIcon} />
                  <TextInput
                    value={values.firstName}
                    onChangeText={handleChange('firstName')}
                    onBlur={handleBlur('firstName')}
                    placeholder="Adınız"
                    placeholderTextColor="#999"
                    style={styles.textInput}
                    autoCapitalize="words"
                  />
                </View>
                {touched.firstName && errors.firstName && (
                  <Text style={styles.errorText}>{String(errors.firstName)}</Text>
                )}
              </View>

              <View style={styles.halfInputContainer}>
                <Text style={styles.label}>Soyad</Text>
                <View style={[styles.inputWrapper, touched.lastName && errors.lastName ? styles.inputError : null]}>
                  <MaterialCommunityIcons name="account" size={20} color="#666" style={styles.inputIcon} />
                  <TextInput
                    value={values.lastName}
                    onChangeText={handleChange('lastName')}
                    onBlur={handleBlur('lastName')}
                    placeholder="Soyadınız"
                    placeholderTextColor="#999"
                    style={styles.textInput}
                    autoCapitalize="words"
                  />
                </View>
                {touched.lastName && errors.lastName && (
                  <Text style={styles.errorText}>{String(errors.lastName)}</Text>
                )}
              </View>
            </View>

            {/* E-posta */}
            <View style={styles.fullInputContainer}>
              <Text style={styles.label}>E-posta</Text>
              <View style={[styles.inputWrapper, touched.email && errors.email ? styles.inputError : null]}>
                <MaterialCommunityIcons name="email" size={20} color="#666" style={styles.inputIcon} />
                <TextInput
                  value={values.email}
                  onChangeText={handleChange('email')}
                  onBlur={handleBlur('email')}
                  placeholder="ornek@email.com"
                  placeholderTextColor="#999"
                  style={styles.textInput}
                  keyboardType="email-address"
                  autoCapitalize="none"
                />
              </View>
              {touched.email && errors.email && (
                <Text style={styles.errorText}>{String(errors.email)}</Text>
              )}
            </View>

            {/* Şifre */}
            <View style={styles.fullInputContainer}>
              <Text style={styles.label}>Şifre</Text>
              <View style={[styles.inputWrapper, touched.password && errors.password ? styles.inputError : null]}>
                <MaterialCommunityIcons name="lock" size={20} color="#666" style={styles.inputIcon} />
                <TextInput
                  value={values.password}
                  onChangeText={handleChange('password')}
                  onBlur={handleBlur('password')}
                  placeholder="••••••••"
                  placeholderTextColor="#999"
                  style={styles.textInput}
                  secureTextEntry={secureTextEntry}
                  autoCapitalize="none"
                />
                <TouchableOpacity onPress={() => setSecureTextEntry(!secureTextEntry)} style={styles.eyeIcon}>
                  <MaterialCommunityIcons name={secureTextEntry ? 'eye-off' : 'eye'} size={20} color="#666" />
                </TouchableOpacity>
              </View>
              {touched.password && errors.password && (
                <Text style={styles.errorText}>{String(errors.password)}</Text>
              )}
            </View>

            {/* Şifre Tekrar */}
            <View style={styles.fullInputContainer}>
              <Text style={styles.label}>Şifre Tekrar</Text>
              <View style={[styles.inputWrapper, touched.confirmPassword && errors.confirmPassword ? styles.inputError : null]}>
                <MaterialCommunityIcons name="lock" size={20} color="#666" style={styles.inputIcon} />
                <TextInput
                  value={values.confirmPassword}
                  onChangeText={handleChange('confirmPassword')}
                  onBlur={handleBlur('confirmPassword')}
                  placeholder="••••••••"
                  placeholderTextColor="#999"
                  style={styles.textInput}
                  secureTextEntry={secureConfirmTextEntry}
                  autoCapitalize="none"
                />
                <TouchableOpacity onPress={() => setSecureConfirmTextEntry(!secureConfirmTextEntry)} style={styles.eyeIcon}>
                  <MaterialCommunityIcons name={secureConfirmTextEntry ? 'eye-off' : 'eye'} size={20} color="#666" />
                </TouchableOpacity>
              </View>
              {touched.confirmPassword && errors.confirmPassword && (
                <Text style={styles.errorText}>{String(errors.confirmPassword)}</Text>
              )}
            </View>

            {/* Kayıt Ol Butonu */}
            <TouchableOpacity
              style={[styles.submitButton, loading && styles.submitButtonDisabled]}
              onPress={() => handleSubmit()}
              disabled={loading}
              activeOpacity={0.8}
            >
              {loading ? (
                <ActivityIndicator color="#FFFFFF" size="small" />
              ) : (
                <Text style={styles.submitButtonText}>Kayıt Ol</Text>
              )}
            </TouchableOpacity>
          </View>
        )}
      </Formik>
    </View>
  );
};

const styles = StyleSheet.create({
  formContainer: {
    width: '100%',
  },
  fieldsWrapper: {
    width: '100%',
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 12,
  },
  halfInputContainer: {
    width: '48%',
  },
  fullInputContainer: {
    width: '100%',
    marginBottom: 12,
  },
  label: {
    fontSize: 13,
    fontWeight: '600',
    color: '#444444',
    marginBottom: 4,
  },
  inputWrapper: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F5F7FA',
    borderWidth: 1,
    borderColor: '#E1E8ED',
    borderRadius: 10,
    paddingHorizontal: 12,
    height: 48,
  },
  inputError: {
    borderColor: '#E53935',
  },
  inputIcon: {
    marginRight: 8,
  },
  textInput: {
    flex: 1,
    fontSize: 15,
    color: '#111111',
    paddingVertical: 8,
  },
  eyeIcon: {
    padding: 4,
  },
  errorText: {
    color: '#E53935',
    fontSize: 11,
    marginTop: 4,
    marginLeft: 2,
  },
  submitButton: {
    backgroundColor: '#00A0E9',
    height: 50,
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 16,
    shadowColor: '#00A0E9',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 3,
  },
  submitButtonDisabled: {
    backgroundColor: '#90CAF9',
  },
  submitButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default RegisterForm;
