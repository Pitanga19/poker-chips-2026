import React from 'react'
import { NativeStackScreenProps } from '@react-navigation/native-stack'
import { RootStackParamList } from '../../../../navigation/AppNavigator'
import { ScreenLayout } from '../../../../layout/ScreenLayout'
import { Form, InputContainer, SubmitContainer } from '../../../../ui/Forms'
import { TextInput, InputLabel, InputError } from '../../../../ui/Inputs'
import { PrimaryButton, ButtonText } from '../../../../ui/Buttons'

type Props = NativeStackScreenProps<RootStackParamList, 'CreateGame'>

export default function CreateGameScreen({ navigation }: Props) {
  const handleBack = () => navigation.goBack()
  
  return (
    <ScreenLayout
      title={'Crear Juego'}
      showBack={true}
      onBack={handleBack}
    >
      <Form>
        <InputContainer>
          <InputLabel>Tamaño de la mesa</InputLabel>
          <TextInput></TextInput>
          <InputError></InputError>
        </InputContainer>
        
        <InputContainer>
          <InputLabel>Su posición en la mesa</InputLabel>
          <TextInput></TextInput>
          <InputError></InputError>
        </InputContainer>
        
        <InputContainer>
          <InputLabel>Stack inicial</InputLabel>
          <TextInput></TextInput>
          <InputError></InputError>
        </InputContainer>
        
        <InputContainer>
          <InputLabel>Valor ciega grande</InputLabel>
          <TextInput></TextInput>
          <InputError></InputError>
        </InputContainer>
        
        <SubmitContainer>
          <PrimaryButton>
            <ButtonText>Crear Juego</ButtonText>
          </PrimaryButton>
        </SubmitContainer>
      </Form>
    </ScreenLayout>
  )
}
