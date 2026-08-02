export const lightColors = {
  primary: '#0EA5E9',         // Sicilius Cyan
  primaryHover: '#0284C7',
  secondary: '#6366F1',       // Indigo
  accent: '#0284C7',
  error: '#EF4444',
  white: '#FFFFFF',
  background: '#F8FAFC',      // Crisp Light Background (Web Design)
  surface: '#FFFFFF',         // Pure White Cards
  card: '#FFFFFF',
  text: '#0F172A',            // Deep Slate Text
  subtext: '#64748B',         // Muted Slate
  success: '#10B981',
  warning: '#F59E0B',
  border: '#E2E8F0',
  placeholder: '#94A3B8',
  disabled: '#94A3B8',
  onSurface: '#0F172A',
  outline: '#E2E8F0',
  outlineVariant: '#CBD5E1',
};

export const darkColors = {
  primary: '#0EA5E9',
  primaryHover: '#0284C7',
  secondary: '#6366F1',
  accent: '#38BDF8',
  error: '#EF4444',
  white: '#FFFFFF',
  background: '#0B0F17',      // Ultra Dark Slate
  surface: '#151C2C',
  card: '#151C2C',
  text: '#F8FAFC',
  subtext: '#94A3B8',
  success: '#10B981',
  warning: '#F59E0B',
  border: 'rgba(255, 255, 255, 0.1)',
  placeholder: '#64748B',
  disabled: '#64748B',
  onSurface: '#F8FAFC',
  outline: 'rgba(255, 255, 255, 0.1)',
  outlineVariant: 'rgba(255, 255, 255, 0.2)',
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
};

export const typography = {
  h1: { fontSize: 24, fontWeight: '700' as const, lineHeight: 32 },
  h2: { fontSize: 20, fontWeight: '600' as const, lineHeight: 28 },
  h3: { fontSize: 18, fontWeight: '600' as const, lineHeight: 24 },
  body: { fontSize: 14, fontWeight: '400' as const, lineHeight: 20 },
  body1: { fontSize: 16, fontWeight: '400' as const, lineHeight: 22 },
  body2: { fontSize: 14, fontWeight: '400' as const, lineHeight: 20 },
  caption: { fontSize: 12, fontWeight: '400' as const, lineHeight: 16 },
};

export const shadows = {
  small: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  medium: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.15,
    shadowRadius: 4,
    elevation: 4,
  },
};

export const lightTheme = {
  colors: lightColors,
  spacing,
  typography,
  shadows,
};

export const darkTheme = {
  colors: darkColors,
  spacing,
  typography,
  shadows,
};

export const theme = lightTheme;
export default lightTheme;
