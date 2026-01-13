import { SafeAreaView } from 'react-native-safe-area-context'
import styled from 'styled-components/native'

export const Screen = styled(SafeAreaView)`
  flex: 1;
  width: 100%;
  height: 100%;
  background-color: ${({ theme }) => theme.colors.background};
`
