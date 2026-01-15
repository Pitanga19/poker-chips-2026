import React from 'react'
import { NativeStackScreenProps } from '@react-navigation/native-stack'
import { RootStackParamList } from '../../../../navigation/AppStack'
import { ScreenLayout } from '../../../../layout/ScreenLayout'
import { Form, InputContainer, SubmitContainer } from '../../../../ui/Forms'
import { TextInput, InputLabel, InputError } from '../../../../ui/Inputs'
import { PrimaryButton, ButtonText } from '../../../../ui/Buttons'

type Props = NativeStackScreenProps<RootStackParamList, 'JoinLobby'>

export default function JoinLobbyScreen({ navigation }: Props) {
  const handleBack = () => navigation.goBack()
  
  return (
    <ScreenLayout title={'Unirse a Juego'} showBack={true} onBack={handleBack}>
      <Form>
        <InputContainer>
          <InputLabel>Código del Juego</InputLabel>
          <TextInput></TextInput>
          <InputError></InputError>
        </InputContainer>
        
        <SubmitContainer>
          <PrimaryButton>
            <ButtonText>Unirse</ButtonText>
          </PrimaryButton>
        </SubmitContainer>
      </Form>
    </ScreenLayout>
  )
}
