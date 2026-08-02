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
import { RootStackParamList } from '../../navigation/types';
import { lightColors } from '../../theme';

const { height } = Dimensions.get('window');

type LoginScreenNavigationProp = NativeStackNavigationProp<RootStackParamList>;

const LoginFooter: React.FC = () => {
  const navigation = useNavigation<LoginScreenNavigationProp>();

  return (
    <View style={styles.registerContainer}>
      <Text style={styles.registerText}>Hesabınız yok mu?</Text>
      <TouchableOpacity onPress={() => (navigation.navigate as any)('Register')}>
        <Text style={styles.registerLink}>Kayıt Ol</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  registerContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: height * 0.03,
  },
  registerText: {
    color: lightColors.subtext,
  },
  registerLink: {
    color: lightColors.primary,
    marginLeft: 4,
    fontWeight: 'bold',
  },
});

export default LoginFooter;
