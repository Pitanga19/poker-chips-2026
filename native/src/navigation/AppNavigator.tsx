import React from 'react'
import { createNativeStackNavigator } from '@react-navigation/native-stack'

export type RootStackParamList = {
}

const Stack = createNativeStackNavigator<RootStackParamList>()

export default function AppNavigator() {
  return (
    <Stack.Navigator
      screenOptions={{ headerShown: false }}
    >
      Hola Poker
    </Stack.Navigator>
  )
}
