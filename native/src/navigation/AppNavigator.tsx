import React from 'react'
import { createNativeStackNavigator } from '@react-navigation/native-stack'
import LoginScreen from '../features/auth/screens/loginScreen/LoginScreen'
import HomeScreen from '../features/home/screens/HomeScreen'
import CreateGameScreen from '../features/lobbies/screens/createGameScreen/CreateGameScreen'
import JoinGameScreen from '../features/lobbies/screens/joinGameScreen/JoinGameScreen'

export type RootStackParamList = {
  Login: undefined
  Home: undefined
  CreateGame: undefined
  JoinGame: undefined
}

const Stack = createNativeStackNavigator<RootStackParamList>()

export default function AppNavigator() {
  return (
    <Stack.Navigator
      screenOptions={{ headerShown: false }}
    >
      <Stack.Screen name='Login' component={LoginScreen} />
      <Stack.Screen name='Home' component={HomeScreen} />
      <Stack.Screen name='CreateGame' component={CreateGameScreen} />
      <Stack.Screen name='JoinGame' component={JoinGameScreen} />
    </Stack.Navigator>
  )
}
