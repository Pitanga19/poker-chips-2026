import React, { useState } from 'react'
import { NativeStackScreenProps } from '@react-navigation/native-stack'
import { LobbyCreateRequest, UserInfo } from '../../types'
import { RootStackParamList } from '../../../../navigation/AppStack'
import { ScreenLayout } from '../../../../layout/ScreenLayout'
import { Form, InputContainer, SubmitContainer } from '../../../../ui/Forms'
import { TextInput, InputLabel, InputError } from '../../../../ui/Inputs'
import { PrimaryButton, ButtonText } from '../../../../ui/Buttons'
import { createLobby } from '../../../../api/lobbies'
import { useAuth } from '../../../auth/hooks/useAuth'

type Props = NativeStackScreenProps<RootStackParamList, 'CreateLobby'>

export default function CreateLobbyScreen({ navigation }: Props) {
  const { user } = useAuth()
  const id = user?.id ?? 0
  const username = user?.username ?? ''
  const [tableSize, setTableSize] = useState<string>('')
  const [bigBlindValue, setBigBlindValue] = useState<string>('')
  const [initialStack, setInitialStack] = useState<string>('')
  const [selfPosition, setSelfPosition] = useState<string>('')
  
  const handleBack = () => navigation.goBack()
  
  const handleSubmit = () => {
    const createLobbyRequest: LobbyCreateRequest = {
      hoster_info: { id, username },
      table_size: parseInt(tableSize),
      big_blind_value: parseInt(bigBlindValue),
      initial_stack: parseInt(initialStack),
      self_position: parseInt(selfPosition),
    }
    
    createLobby(createLobbyRequest)
  }
  
  return (
    <ScreenLayout title={'Crear Juego'} showBack={true} onBack={handleBack}>
      <Form>
        <InputContainer>
          <InputLabel>Cantidad de asientos</InputLabel>
          <TextInput
            placeholder='2 a 10'
            value={tableSize}
            onChangeText={setTableSize}
          />
          <InputError></InputError>
        </InputContainer>
        
        <InputContainer>
          <InputLabel>Valor de la ciega grande</InputLabel>
          <TextInput
            placeholder='valor en fichas'
            value={bigBlindValue}
            onChangeText={setBigBlindValue}
          />
          <InputError></InputError>
        </InputContainer>
        
        <InputContainer>
          <InputLabel>Stack inicial</InputLabel>
          <TextInput
            placeholder='fichas iniciales'
            value={initialStack}
            onChangeText={setInitialStack}
          />
          <InputError></InputError>
        </InputContainer>
        
        <InputContainer>
          <InputLabel>Su posición en la mesa</InputLabel>
          <TextInput
            placeholder='número de asiento'
            value={selfPosition}
            onChangeText={setSelfPosition}
          />
          <InputError></InputError>
        </InputContainer>
        
        <SubmitContainer>
          <PrimaryButton onPress={handleSubmit}>
            <ButtonText>Crear Juego</ButtonText>
          </PrimaryButton>
        </SubmitContainer>
      </Form>
    </ScreenLayout>
  )
}
