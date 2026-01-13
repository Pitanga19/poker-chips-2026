import { ReactNode } from 'react'
import { StatusBar } from 'react-native'

type Props = {
  children: ReactNode
}

export const GlobalStyle = ({ children }: Props) => {
  return (
    <>
      <StatusBar
        translucent
        backgroundColor='transparent'
        barStyle='light-content'
      />
      {children}
    </>
  )
}
