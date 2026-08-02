import React from 'react';
import { View, StyleSheet, Text, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { ProfileStackNavigationProp } from '../../navigation/types';
import { lightColors } from '../../theme';

const ProfileScreen = () => {
  const navigation = useNavigation<ProfileStackNavigationProp>();

  return (
    <View style={styles.container}>
      <TouchableOpacity
        onPress={() => navigation.goBack()}
        style={styles.backButton}
      >
        <Text style={styles.backButtonText}>Geri Dön</Text>
      </TouchableOpacity>
      <View style={styles.content}>
        <Text style={styles.titleText}>Profil Ekranı</Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: lightColors.background,
  },
  backButton: {
    padding: 16,
    alignItems: 'center',
  },
  backButtonText: {
    color: lightColors.primary,
    fontWeight: 'bold',
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  titleText: {
    fontSize: 16,
    color: lightColors.text,
  },
});

export default ProfileScreen;
