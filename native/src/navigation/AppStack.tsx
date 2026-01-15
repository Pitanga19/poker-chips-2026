import { createNativeStackNavigator } from '@react-navigation/native-stack'
import HomeScreen from '../features/home/HomeScreen'
import CreateLobbyScreen from '../features/lobbies/screens/createLobbyScreen/CreateLobbyScreen'
import JoinLobbyScreen from '../features/lobbies/screens/joinLobbyScreen/JoinLobbyScreen'

export type RootStackParamList = {
  Home: undefined
  CreateLobby: undefined
  JoinLobby: undefined
}

const Stack = createNativeStackNavigator<RootStackParamList>()

export function AppStack() {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name='Home' component={HomeScreen} />
      <Stack.Screen name='CreateLobby' component={CreateLobbyScreen} />
      <Stack.Screen name='JoinLobby' component={JoinLobbyScreen} />
    </Stack.Navigator>
  )
}
