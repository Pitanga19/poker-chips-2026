import React from 'react'
import { createNativeStackNavigator } from '@react-navigation/native-stack'
import HomeScreen from '../features/home/screens/HomeScreen'

export type RootStackParamList = {
  Home: undefined
}

const Stack = createNativeStackNavigator<RootStackParamList>()

export default function AppNavigator() {
  return (
    <Stack.Navigator
      screenOptions={{ headerShown: false }}
    >
      <Stack.Screen name='Home' component={HomeScreen} />
    </Stack.Navigator>
  )
}
