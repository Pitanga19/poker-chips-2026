import { createNativeStackNavigator } from '@react-navigation/native-stack'
import HomeScreen from '../features/home/HomeScreen'
import CreateLobbyScreen from '../features/lobbies/screens/createLobbyScreen/CreateLobbyScreen'
import JoinLobbyScreen from '../features/lobbies/screens/joinLobbyScreen/JoinLobbyScreen'
import ProfileScreen from '../features/profile/ProfileScreen'

export type RootStackParamList = {
  Home: undefined
  CreateLobby: undefined
  JoinLobby: undefined
  Profile: undefined
}

const Stack = createNativeStackNavigator<RootStackParamList>()

export function AppStack() {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name='Home' component={HomeScreen} />
      <Stack.Screen name='CreateLobby' component={CreateLobbyScreen} />
      <Stack.Screen name='JoinLobby' component={JoinLobbyScreen} />
      <Stack.Screen name='Profile' component={ProfileScreen} />
    </Stack.Navigator>
  )
}
