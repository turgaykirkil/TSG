import React from 'react';
import { View, StyleSheet, Dimensions, Text } from 'react-native';
import { lightColors } from '../../theme';

const { width, height } = Dimensions.get('window');

const ForgotPasswordHeader: React.FC = () => {
  return (
    <View style={styles.headerContainer}>
      <Text style={styles.headerText}>Şifrenizi mi Unuttunuz?</Text>
      <Text style={styles.subHeaderText}>
        E-posta adresinizi girin, şifrenizi sıfırlamanız için size talimatları gönderelim.
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  headerContainer: {
    alignItems: 'center',
    marginVertical: height * 0.04,
  },
  headerText: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: height * 0.015,
    textAlign: 'center',
    color: lightColors.primary,
  },
  subHeaderText: {
    fontSize: 14,
    marginBottom: height * 0.02,
    textAlign: 'center',
    color: lightColors.subtext,
    paddingHorizontal: width * 0.08,
    lineHeight: 20,
  },
});

export default ForgotPasswordHeader;
