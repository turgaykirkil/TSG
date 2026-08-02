import React from 'react';
import { View, StyleSheet, Text } from 'react-native';
import Svg, { Path } from 'react-native-svg';

interface SiciliusLogoProps {
  size?: number;
  showText?: boolean;
  textColor?: string;
}

export const SiciliusLogo: React.FC<SiciliusLogoProps> = ({
  size = 56,
  showText = true,
  textColor = '#0EA5E9',
}) => {
  return (
    <View style={styles.container}>
      <Svg viewBox="0 0 24 24" width={size} height={size} fill="none">
        <Path
          d="M15.6 12.8c-1.2 1.2-2.8 2-4.6 2s-3.4-.8-4.6-2c-1.2-1.2-2-2.8-2-4.6s.8-3.4 2-4.6c1.2-1.2 2.8-2 4.6-2s3.4.8 4.6 2"
          stroke="#0EA5E9"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <Path
          d="M8.4 11.2c1.2-1.2 2.8-2 4.6-2s3.4.8 4.6 2c1.2 1.2 2 2.8 2 4.6s-.8 3.4-2 4.6c-1.2 1.2-2.8 2-4.6 2s-3.4-.8-4.6-2"
          stroke="#0EA5E9"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </Svg>

      {showText && (
        <Text style={[styles.brandText, { color: textColor }]}>
          Sicilius
        </Text>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
    flexDirection: 'row',
  },
  brandText: {
    fontSize: 32,
    fontWeight: '700',
    color: '#0EA5E9',
    marginLeft: 12,
    letterSpacing: 0.5,
  },
});

export default SiciliusLogo;
