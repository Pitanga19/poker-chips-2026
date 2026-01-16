import { useState } from 'react'
import { useAuth } from '../../hooks/useAuth'
import { NativeStackScreenProps } from '@react-navigation/native-stack'
import { RootStackParamList } from '../../../../navigation/AuthStack'
import { ScreenLayout } from '../../../../layout/ScreenLayout'
import { LogoContainer, LogoImage } from '../../../../ui/Logo'
import { Form, InputContainer, SubmitContainer } from '../../../../ui/Forms'
import { TextInput, InputLabel, InputError } from '../../../../ui/Inputs'
import { PrimaryButton, ButtonText } from '../../../../ui/Buttons'
import { Container } from '../AuthScreen.styles'

type Props = NativeStackScreenProps<RootStackParamList, 'Register'>

export default function RegisterScreen({ navigation }: Props) {
  const { register } = useAuth()
  const [username, setUsername] = useState<string>('')
  const [usernameError, setUsernameError] = useState<string | null>(null)
  const [password, setPassword] = useState<string>('')
  const [passwordError, setPasswordError] = useState<string | null>(null)
  const [password_confirm, setPasswordConfirm] = useState<string>('')
  const [passwordConfirmError, setPasswordConfirmError] = useState<string | null>(null)
  const [registerError, setRegisterError] = useState<string | null>(null)
  
  const handleBack = () => navigation.goBack()
  
  const handleSubmit = async () => {
    try {
      await register({ username, password, password_confirm })
    } catch {
      setRegisterError('Usuario o contraseña inválidos')
    }
  }
  
  return (
    <ScreenLayout title={'Registrarse'} showBack={true} onBack={handleBack}>
      <Container>
        <LogoContainer>
          <LogoImage
            source={require('../../../../assets/logo.png')}
            resizeMode='contain'
          />
        </LogoContainer>
        <Form>
          <InputContainer>
            <InputLabel>Nombre de Usuario</InputLabel>
            <TextInput
              placeholder='nombre de usuario'
              value={username}
              onChangeText={setUsername}
            />
            {usernameError && <InputError>{usernameError}</InputError>}
          </InputContainer>
          
          <InputContainer>
            <InputLabel>Contraseña</InputLabel>
            <TextInput
              placeholder='contraseña'
              value={password}
              onChangeText={setPassword}
              secureTextEntry
              autoCapitalize='none'
              autoCorrect={false}
              textContentType='password'
              />
            {passwordError && <InputError>{passwordError}</InputError>}
          </InputContainer>
          
          <InputContainer>
            <InputLabel>Confirmar contraseña</InputLabel>
            <TextInput
              placeholder='confirmar contraseña'
              value={password_confirm}
              onChangeText={setPasswordConfirm}
              secureTextEntry
              autoCapitalize='none'
              autoCorrect={false}
              textContentType='password'
            />
            {passwordError && <InputError>{passwordConfirmError}</InputError>}
          </InputContainer>
          
          <SubmitContainer>
            {registerError && <InputError>{registerError}</InputError>}
            <PrimaryButton onPress={() => handleSubmit()}>
              <ButtonText>Registrarme</ButtonText>
            </PrimaryButton>
          </SubmitContainer>
        </Form>
      </Container>
    </ScreenLayout>
  )
}
