import { ImageBackground } from 'react-native'
import styled from 'styled-components/native'

const Container = styled(ImageBackground)`
  flex: 1;
  width: 100%;
  height: 100%;
  justify-content: center;
  align-items: center;
`

export const LoaderLayout = () => {
  return (
    <Container
      source={require('../assets/splash.png')}
      resizeMode='cover'
    />
  )
}
