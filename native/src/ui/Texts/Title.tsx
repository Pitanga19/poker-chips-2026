import styled from 'styled-components/native'
import { Text } from './Text'

export const Title = styled(Text)`
  font-size: ${({ theme }) => theme.typography.sizes.lg}px;
  font-weight: ${({ theme }) => theme.typography.weights.bold};
`
