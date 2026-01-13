import React from 'react'
import { NativeStackScreenProps } from '@react-navigation/native-stack'
import { RootStackParamList } from '../../../navigation/AppNavigator'
import { Container, LogoContainer, LogoImage, Actions } from './HomeScreen.styles'
import { ScreenLayout } from '../../../layout/ScreenLayout'
import { PrimaryButton, ButtonText } from '../../../ui/Buttons'

type Props = NativeStackScreenProps<RootStackParamList, 'Home'>

export default function HomeScreen({ navigation }: Props) {
  return (
    <ScreenLayout>
      <Container>
        <LogoContainer>
          <LogoImage source={require('../../../assets/logo.png')} resizeMode='contain' />
        </LogoContainer>
        
        <Actions>
          <PrimaryButton onPress={() => navigation.navigate('CreateGame')}>
            <ButtonText>Crear Juego</ButtonText>
          </PrimaryButton>
          
          <PrimaryButton>
            <ButtonText>Unirse a Juego</ButtonText>
          </PrimaryButton>
          
          <PrimaryButton>
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
