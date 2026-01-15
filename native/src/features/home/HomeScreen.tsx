import React from 'react'
import { useAuth } from '../auth/hooks/useAuth'
import { NativeStackScreenProps } from '@react-navigation/native-stack'
import { RootStackParamList } from '../../navigation/AppStack'
import { ScreenLayout } from '../../layout/ScreenLayout'
import { Container, Actions } from './HomeScreen.styles'
import { LogoContainer, LogoImage } from '../../ui/Logo'
import { Title } from '../../ui/Texts'
import { PrimaryButton, ButtonText } from '../../ui/Buttons'

type Props = NativeStackScreenProps<RootStackParamList, 'Home'>

export default function HomeScreen({ navigation }: Props) {
  const { user } = useAuth()
  const username = user?.username ?? ''

  return (
    <ScreenLayout>
      <Container>
        <LogoContainer>
          <LogoImage
            source={require('../../assets/logo.png')}
            resizeMode='contain'
          />
          <Title>¡Hola, {username}!</Title>
        </LogoContainer>
        
        <Actions>
          <PrimaryButton onPress={() => navigation.navigate('CreateLobby')}>
            <ButtonText>Crear Juego</ButtonText>
          </PrimaryButton>
          
          <PrimaryButton onPress={() => navigation.navigate('JoinLobby')}>
            <ButtonText>Unirse a Juego</ButtonText>
          </PrimaryButton>
          
          <PrimaryButton onPress={() => navigation.navigate('Profile')}>
            <ButtonText>Perfil</ButtonText>
          </PrimaryButton>
          
          <PrimaryButton>
            <ButtonText>Configuración</ButtonText>
          </PrimaryButton>
        </Actions>
      </Container>
    </ScreenLayout>
  )
}
