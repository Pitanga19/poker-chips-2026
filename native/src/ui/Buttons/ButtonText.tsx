import styled from 'styled-components/native'

export const ButtonText = styled.Text`
  text-transform: uppercase;
  color: ${({ theme }) => theme.colors.buttonText};
  font-size: ${({ theme }) => theme.typography.sizes.sm}px;
  font-weight: ${({ theme }) => theme.typography.weights.medium};
`
