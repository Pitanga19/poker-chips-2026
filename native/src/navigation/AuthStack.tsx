import { createNativeStackNavigator } from '@react-navigation/native-stack'
import LoginScreen from '../features/auth/screens/loginScreen/LoginScreen'
import RegisterScreen from '../features/auth/screens/registerScreen/RegisterScreen'

export type RootStackParamList = {
  Login: undefined
  Register: undefined
}

const Stack = createNativeStackNavigator<RootStackParamList>()

export function AuthStack() {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name='Login' component={LoginScreen} />
      <Stack.Screen name='Register' component={RegisterScreen} />
    </Stack.Navigator>
  )
}
