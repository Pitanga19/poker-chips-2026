import styled from 'styled-components/native'
import { Text } from './Text'

export const ErrorText = styled(Text)`
  color: ${({ theme }) => theme.colors.buttonBackground};
  font-size: ${({ theme }) => theme.typography.sizes.sm}px;
`
