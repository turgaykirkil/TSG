import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';
import { Formik } from 'formik';
import * as Yup from 'yup';
import { MaterialCommunityIcons as Icon } from '@expo/vector-icons';

const validationSchema = Yup.object().shape({
  email: Yup.string()
    .email('Geçersiz e-posta adresi')
    .required('E-posta adresi gerekli'),
});

interface ForgotPasswordFormProps {
  onPasswordResetRequest: (email: string) => Promise<void>;
}

const ForgotPasswordForm: React.FC<ForgotPasswordFormProps> = ({ onPasswordResetRequest }) => {
  const [isEmailSent, setIsEmailSent] = useState(false);

  const handleResetPassword = async (values: { email: string }, { setSubmitting }: any) => {
    try {
      await onPasswordResetRequest(values.email);
      setIsEmailSent(true);
    } catch (error) {
      console.error('Password reset failed:', error);
    } finally {
      setSubmitting(false);
    }
  };

  if (isEmailSent) {
    return (
      <View style={styles.successContainer}>
        <Icon name="check-circle-outline" size={56} color="#10B981" style={{ marginBottom: 16 }} />
        <Text style={styles.successText}>
          Şifre sıfırlama talimatları e-posta adresinize gönderildi. Lütfen gelen kutunuzu kontrol edin.
        </Text>
      </View>
    );
  }

  return (
    <Formik
      initialValues={{ email: '' }}
      validationSchema={validationSchema}
      onSubmit={handleResetPassword}
    >
      {({
        handleChange,
        handleBlur,
        handleSubmit,
        values,
        errors,
        touched,
        isSubmitting,
      }) => (
        <View style={styles.formContainer}>
          <View style={styles.inputGroup}>
            <Text style={styles.label}>E-posta Adresi</Text>
            <View style={[styles.inputWrapper, touched.email && errors.email ? styles.inputError : null]}>
              <Icon name="email-outline" size={20} color="#6B7280" style={styles.inputIcon} />
              <TextInput
                style={styles.input}
                value={values.email}
                onChangeText={handleChange('email')}
                onBlur={handleBlur('email')}
                keyboardType="email-address"
                autoCapitalize="none"
                placeholder="Örn: kullanici@sicilius.com.tr"
                placeholderTextColor="#9CA3AF"
              />
            </View>
            {touched.email && errors.email ? (
              <Text style={styles.errorText}>{errors.email}</Text>
            ) : null}
          </View>

          <TouchableOpacity
            style={styles.button}
            activeOpacity={0.8}
            onPress={() => handleSubmit()}
            disabled={isSubmitting}
          >
            <Text style={styles.buttonLabel}>
              {isSubmitting ? 'Gönderiliyor...' : 'Şifre Sıfırlama Bağlantısı Gönder'}
            </Text>
          </TouchableOpacity>
        </View>
      )}
    </Formik>
  );
};

const styles = StyleSheet.create({
  formContainer: {
    marginTop: 16,
    paddingHorizontal: 20,
  },
  inputGroup: {
    marginBottom: 16,
  },
  label: {
    fontSize: 13,
    fontWeight: '600',
    color: '#374151',
    marginBottom: 6,
  },
  inputWrapper: {
    flexDirection: 'row',
    alignItems: 'center',
    height: 48,
    borderWidth: 1,
    borderColor: '#D1D5DB',
    borderRadius: 10,
    paddingHorizontal: 12,
    backgroundColor: '#FFFFFF',
  },
  inputIcon: {
    marginRight: 10,
  },
  input: {
    flex: 1,
    fontSize: 15,
    color: '#1F2937',
  },
  inputError: {
    borderColor: '#EF4444',
  },
  errorText: {
    color: '#EF4444',
    fontSize: 12,
    marginTop: 4,
  },
  button: {
    height: 48,
    borderRadius: 10,
    backgroundColor: '#00A0E9',
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 12,
  },
  buttonLabel: {
    fontSize: 15,
    fontWeight: 'bold',
    color: '#FFFFFF',
  },
  successContainer: {
    marginTop: 32,
    alignItems: 'center',
    paddingHorizontal: 24,
  },
  successText: {
    fontSize: 15,
    color: '#10B981',
    textAlign: 'center',
    lineHeight: 22,
  },
});

export default ForgotPasswordForm;
