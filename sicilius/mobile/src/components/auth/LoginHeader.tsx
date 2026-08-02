import React from 'react';
import { View, StyleSheet, Dimensions, Text } from 'react-native';
import SiciliusLogo from '../common/SiciliusLogo';
import { lightColors } from '../../theme';

const { height } = Dimensions.get('window');

const LoginHeader: React.FC = () => {
  return (
    <View style={styles.headerContainer}>
      <View style={styles.logoRow}>
        <SiciliusLogo size={44} showText={true} textColor={lightColors.primary} />
      </View>
      <Text style={styles.subtitle}>
        Hesabınıza giriş yapın
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  headerContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: height * 0.05,
    marginBottom: height * 0.03,
  },
  logoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  subtitle: {
    fontSize: 15,
    marginTop: 10,
    fontWeight: '500',
    color: lightColors.subtext,
  },
});

export default LoginHeader;
