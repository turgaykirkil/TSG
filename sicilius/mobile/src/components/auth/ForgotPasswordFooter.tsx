import React from 'react';
import {
  View,
  StyleSheet,
  TouchableOpacity,
  Dimensions,
  Text,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { AuthStackParamList } from '../../navigation/types';
import { lightColors } from '../../theme';

const { height } = Dimensions.get('window');

type ForgotPasswordScreenNavigationProp = NativeStackNavigationProp<AuthStackParamList, 'ForgotPassword'>;

const ForgotPasswordFooter: React.FC = () => {
  const navigation = useNavigation<ForgotPasswordScreenNavigationProp>();

  return (
    <View style={styles.loginContainer}>
      <Text style={styles.loginText}>Hesabınıza geri dönmek mi istiyorsunuz?</Text>
      <TouchableOpacity onPress={() => navigation.navigate('Login')}>
        <Text style={styles.loginLink}>Giriş Yap</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  loginContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: height * 0.04,
  },
  loginText: {
    color: lightColors.subtext,
    fontSize: 14,
  },
  loginLink: {
    color: lightColors.primary,
    marginLeft: 4,
    fontSize: 14,
    fontWeight: 'bold',
  },
});

export default ForgotPasswordFooter;
