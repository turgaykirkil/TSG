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

type RegisterScreenNavigationProp = NativeStackNavigationProp<AuthStackParamList, 'Register'>;

const RegisterFooter: React.FC = () => {
  const navigation = useNavigation<RegisterScreenNavigationProp>();

  return (
    <View style={styles.loginContainer}>
      <Text style={styles.loginText}>Zaten bir hesabınız var mı?</Text>
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
    marginTop: height * 0.02,
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

export default RegisterFooter;
