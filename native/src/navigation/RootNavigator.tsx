import { createNativeStackNavigator } from '@react-navigation/native-stack'
import { useAuth } from '../features/auth/hooks/useAuth'
import { AppStack } from './AppStack'
import { AuthStack } from './AuthStack'

const Stack = createNativeStackNavigator()

export default function RootNavigator() {
  const { isAuthenticated } = useAuth()
  
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      {isAuthenticated ? (
        <Stack.Screen name='App' component={AppStack} />
      ) : (
        <Stack.Screen name='Auth' component={AuthStack} />
      )}
    </Stack.Navigator>
  )
}
