import React from 'react'
import { TouchableOpacity, TouchableOpacityProps } from 'react-native'
import { Ionicons } from '@expo/vector-icons'

type Props = TouchableOpacityProps & {
  icon: keyof typeof Ionicons.glyphMap
  size?: number
  color?: string
}

export const IconButton = ({
  icon,
  size = 24,
  color = '#fff',
  ...rest
}: Props) => {
  return (
    <TouchableOpacity {...rest}>
      <Ionicons
        name={icon}
        size={size}
        color={color}
      />
    </TouchableOpacity>
  )
}
