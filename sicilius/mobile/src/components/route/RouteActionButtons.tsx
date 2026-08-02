import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ActivityIndicator } from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';

interface RouteActionButtonsProps {
  selectedPointsCount: number;
  isLoading: boolean;
  onCalculateRoute: () => void;
  onClearSelection: () => void;
}

const RouteActionButtons: React.FC<RouteActionButtonsProps> = ({
  selectedPointsCount,
  isLoading,
  onCalculateRoute,
  onClearSelection,
}) => {
  const isCalcDisabled = selectedPointsCount < 1 || isLoading;
  const isClearDisabled = selectedPointsCount === 0 || isLoading;

  return (
    <View style={styles.container}>
      <TouchableOpacity
        style={[styles.calcBtn, isCalcDisabled ? styles.disabledBtn : null]}
        onPress={onCalculateRoute}
        disabled={isCalcDisabled}
      >
        {isLoading ? (
          <ActivityIndicator size="small" color="#FFFFFF" />
        ) : (
          <>
            <MaterialCommunityIcons name="map-marker-path" size={20} color="#FFFFFF" style={{ marginRight: 6 }} />
            <Text style={styles.calcBtnText}>Rotayı Hesapla</Text>
          </>
        )}
      </TouchableOpacity>

      <TouchableOpacity
        style={[styles.clearBtn, isClearDisabled ? styles.disabledBtn : null]}
        onPress={onClearSelection}
        disabled={isClearDisabled}
      >
        <MaterialCommunityIcons name="close" size={20} color="#00A0E9" style={{ marginRight: 4 }} />
        <Text style={styles.clearBtnText}>Temizle</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  calcBtn: {
    flex: 0.65,
    height: 44,
    borderRadius: 10,
    backgroundColor: '#00A0E9',
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 8,
  },
  calcBtnText: {
    color: '#FFFFFF',
    fontWeight: 'bold',
    fontSize: 14,
  },
  clearBtn: {
    flex: 0.35,
    height: 44,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#00A0E9',
    backgroundColor: '#FFFFFF',
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  clearBtnText: {
    color: '#00A0E9',
    fontWeight: '600',
    fontSize: 14,
  },
  disabledBtn: {
    opacity: 0.5,
  },
});

export default React.memo(RouteActionButtons);
