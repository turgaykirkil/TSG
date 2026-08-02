import React from 'react';
import {
  View,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  StatusBar,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import ForgotPasswordHeader from '../../components/auth/ForgotPasswordHeader';
import ForgotPasswordForm from '../../components/auth/ForgotPasswordForm';
import ForgotPasswordFooter from '../../components/auth/ForgotPasswordFooter';
import { lightColors } from '../../theme';

const ForgotPasswordScreen = () => {
  const handlePasswordReset = async (email: string) => {
    try {
      // Password reset request logic
      Alert.alert('Başarılı', `${email} adresine şifre sıfırlama bağlantısı gönderildi.`);
    } catch (error) {
      Alert.alert('Hata', 'Şifre sıfırlama talebi gönderilemedi.');
    }
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle="dark-content" backgroundColor={lightColors.background} />
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.container}
      >
        <ScrollView
          contentContainerStyle={styles.scrollContent}
          keyboardShouldPersistTaps="handled"
          showsVerticalScrollIndicator={false}
        >
          <ForgotPasswordHeader />
          <ForgotPasswordForm onPasswordResetRequest={handlePasswordReset} />
          <ForgotPasswordFooter />
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: lightColors.background,
  },
  container: {
    flex: 1,
  },
  scrollContent: {
    flexGrow: 1,
    justifyContent: 'center',
    paddingHorizontal: 20,
    paddingVertical: 16,
  },
});

export default ForgotPasswordScreen;
