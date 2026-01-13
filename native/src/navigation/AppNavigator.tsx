import React from 'react'
import { createNativeStackNavigator } from '@react-navigation/native-stack'
import HomeScreen from '../features/home/screens/HomeScreen'
import CreateGameScreen from '../features/lobbies/screens/createGameScreen/CreateGameScreen'

export type RootStackParamList = {
  Home: undefined
  CreateGame: undefined
}

const Stack = createNativeStackNavigator<RootStackParamList>()

export default function AppNavigator() {
  return (
    <Stack.Navigator
      screenOptions={{ headerShown: false }}
    >
      <Stack.Screen name='Home' component={HomeScreen} />
      <Stack.Screen name='CreateGame' component={CreateGameScreen} />
    </Stack.Navigator>
  )
}
