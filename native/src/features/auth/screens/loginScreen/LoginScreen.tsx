import { useState } from 'react'
import { useAuth } from '../../hooks/useAuth'
import { Ionicons } from '@expo/vector-icons'
import { NativeStackScreenProps } from '@react-navigation/native-stack'
import { RootStackParamList } from '../../../../navigation/AuthStack'
import { ScreenLayout } from '../../../../layout/ScreenLayout'
import { LogoContainer, LogoImage } from '../../../../ui/Logo'
import { Form, InputContainer, SubmitContainer } from '../../../../ui/Forms'
import { TextInput, InputLabel, InputError } from '../../../../ui/Inputs'
import {
  PrimaryButton,
  SecondaryButton,
  ButtonText,
} from '../../../../ui/Buttons'
import { Container, SecondaryButtonContainer } from '../AuthScreen.styles'

type Props = NativeStackScreenProps<RootStackParamList, 'Login'>

export default function LoginScreen({ navigation }: Props) {
  const { login } = useAuth()
  const [username, setUsername] = useState<string>('')
  const [usernameError, setUsernameError] = useState<string | null>(null)
  const [password, setPassword] = useState<string>('')
  const [passwordError, setPasswordError] = useState<string | null>(null)
  const [loginError, setLoginError] = useState<string | null>(null)

  const handleSubmit = async () => {
    try {
      await login({ username, password })
    } catch {
      setLoginError('Usuario o contraseña inválidos')
    }
  }

  return (
    <ScreenLayout>
      <Container>
        <LogoContainer>
          <LogoImage
            source={require('../../../../assets/logo.png')}
            resizeMode='contain'
          />
        </LogoContainer>
        <Form>
          <InputContainer>
            <InputLabel>Username</InputLabel>
            <TextInput
              placeholder='username'
              value={username}
              onChangeText={setUsername}
            />
            {usernameError && <InputError>{usernameError}</InputError>}
          </InputContainer>
          
          <InputContainer>
            <InputLabel>Password</InputLabel>
            <TextInput
              placeholder='password'
              value={password}
              onChangeText={setPassword}
              />
            {passwordError && <InputError>{passwordError}</InputError>}
          </InputContainer>
          
          <SubmitContainer>
            {loginError && <InputError>{loginError}</InputError>}
            <SecondaryButtonContainer>
              <SecondaryButton>
                <ButtonText>
                  <Ionicons name='help-circle' size={16} /> Olvidé mi contraseña
                </ButtonText>
              </SecondaryButton>
              <SecondaryButton onPress={() => navigation.navigate('Register')}>
                <ButtonText>
                  Registrarme <Ionicons name='add-circle' size={16} />
                </ButtonText>
              </SecondaryButton>
            </SecondaryButtonContainer>
            <PrimaryButton onPress={() => handleSubmit()}>
              <ButtonText>Login</ButtonText>
            </PrimaryButton>
          </SubmitContainer>
        </Form>
      </Container>
    </ScreenLayout>
  )
}
