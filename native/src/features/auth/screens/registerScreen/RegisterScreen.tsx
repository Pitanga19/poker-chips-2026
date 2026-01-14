import { useState, useEffect } from 'react'
import { useAuth } from '../../hooks/useAuth'
import { Ionicons } from '@expo/vector-icons'
import { NativeStackScreenProps } from '@react-navigation/native-stack'
import { RootStackParamList } from '../../../../navigation/AppNavigator'
import { ScreenLayout } from '../../../../layout/ScreenLayout'
import { LogoContainer, LogoImage } from '../../../../ui/Logo'
import { Form, InputContainer, SubmitContainer } from '../../../../ui/Forms'
import { TextInput, InputLabel, InputError } from '../../../../ui/Inputs'
import { PrimaryButton, SecondaryButton, ButtonText } from '../../../../ui/Buttons'
import { Container, SecondaryButtonContainer } from '../AuthScreen.styles'

type Props = NativeStackScreenProps<RootStackParamList, 'Register'>

export default function RegisterScreen({ navigation }: Props) {
  const { register, isAuthenticated } = useAuth()
  const [username, setUsername] = useState<string>('')
  const [usernameError, setUsernameError] = useState<string | null>(null)
  const [password, setPassword] = useState<string>('')
  const [passwordError, setPasswordError] = useState<string | null>(null)
  const [password_confirm, setPasswordConfirm] = useState<string>('')
  const [passwordConfirmError, setPasswordConfirmError] = useState<string | null>(null)
  const [registerError, setRegisterError] = useState<string | null>(null)
  
  const handleSuccessRegister = () => {
    navigation.navigate('Home')
  }
  
  const handleSubmit = async () => {
    setUsernameError(null)
    setPasswordError(null)
    setPasswordConfirmError(null)
    setRegisterError(null)
    
    try {
      await register({ username, password, password_confirm })
    } catch {
      setRegisterError('Usuario o contraseña inválidos')
    }
  }
  
  useEffect(() => {
    if (isAuthenticated) handleSuccessRegister()
  }, [isAuthenticated])
  
  const handleBack = () => navigation.goBack()
  
  return (
    <ScreenLayout
      title={'Registrarse'}
      showBack={true}
      onBack={handleBack}
    >
      <Container>
        <LogoContainer>
          <LogoImage source={require('../../../../assets/logo.png')} resizeMode='contain' />
        </LogoContainer>
        <Form>
          <InputContainer>
            <InputLabel>Usuario</InputLabel>
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
            />
            {passwordError && <InputError>{passwordError}</InputError>}
          </InputContainer>
          
          <InputContainer>
            <InputLabel>Confirmar contraseña</InputLabel>
            <TextInput
              placeholder='confirmar contraseña'
              value={password_confirm}
              onChangeText={setPasswordConfirm}
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
