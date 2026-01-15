import React from 'react'
import { useAuth } from '../auth/hooks/useAuth'
import { NativeStackScreenProps } from '@react-navigation/native-stack'
import { KeyValue } from '../../common/types'
import { RootStackParamList } from '../../navigation/AppStack'
import { ScreenLayout } from '../../layout/ScreenLayout'
import { Container } from './ProfileScreen.styles'
import { LogoContainer, LogoImage } from '../../ui/Logo'
import { ListContainer, ItemContainer, ItemLabel, ItemValue } from '../../ui/Lists'
import { SubmitContainer } from '../../ui/Forms'
import { PrimaryButton, ButtonText } from '../../ui/Buttons'

type Props = NativeStackScreenProps<RootStackParamList, 'Profile'>

export default function ProfileScreen({ navigation }: Props) {
  const { user, logout } = useAuth()
  
  const id: KeyValue = {
    label: 'ID',
    value: user?.id.toString() ?? ''
  }
  const username: KeyValue = {
    label: 'Username',
    value: user?.username ?? ''
  }
  
  const data: KeyValue[] = [id, username]
  
  return (
    <ScreenLayout
    title={'Mi perfil'}
    showBack={true}
    onBack={() => navigation.goBack()}
    >
      <Container>
        <LogoContainer>
          <LogoImage
            source={require('../../assets/logo.png')}
            resizeMode='contain'
          />
        </LogoContainer>
        
        <ListContainer>
          {data.map((item, index) => { return (
            <ItemContainer key={index}>
              <ItemLabel>{item.label}</ItemLabel>
              <ItemValue>{item.value}</ItemValue>
            </ItemContainer>
          )})}
        </ListContainer>
        
        <SubmitContainer>
          <PrimaryButton onPress={ logout }>
            <ButtonText>Cerrar Sesión</ButtonText>
          </PrimaryButton>
        </SubmitContainer>
      </Container>
    </ScreenLayout>
  )
}
