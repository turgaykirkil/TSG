import { NavigatorScreenParams } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';

export type AuthStackParamList = {
  Login: undefined;
  Register: undefined;
  ForgotPassword: undefined;
};

export type RootStackParamList = {
  Auth: NavigatorScreenParams<AuthStackParamList>;
  Main: undefined;
  Profile: undefined;
};

export type RootStackNavigationProp = NativeStackNavigationProp<RootStackParamList>;
export type AuthStackNavigationProp = NativeStackNavigationProp<AuthStackParamList>;

export type MainTabParamList = {
  Home: undefined;
  Tasks: undefined;
  Map: undefined;
  Route: undefined;
  Customers: undefined;
  Settings: undefined;
};

export type TaskStackParamList = {
  TaskList: undefined;
  TaskDetail: { taskId: string };
  NewTask: undefined;
  EditTask: { taskId: string };
};

export type CustomerStackParamList = {
  CustomerList: undefined;
  CustomerDetail: { customerId: string };
  NewCustomer: undefined;
  EditCustomer: { customerId: string };
  CustomerMap: undefined;
  CustomerAnalytics: undefined;
  Map: undefined;
};

export type ProfileStackParamList = {
  ProfileMain: undefined;
  ProfileEdit: undefined;
  ProfileSettings: undefined;
};

export type SettingsStackParamList = {
  SettingsList: undefined;
};

export type TaskStackNavigationProp = NativeStackNavigationProp<TaskStackParamList>;
export type CustomerStackNavigationProp = NativeStackNavigationProp<CustomerStackParamList>;
export type ProfileStackNavigationProp = NativeStackNavigationProp<ProfileStackParamList>;
export type SettingsStackNavigationProp = NativeStackNavigationProp<SettingsStackParamList>;
export type MainScreenNavigationProp = NativeStackNavigationProp<RootStackParamList>;

export type TaskScreenNavigationProp = NativeStackNavigationProp<
  MainTabParamList & TaskStackParamList & CustomerStackParamList
>;
