import styled from 'styled-components/native'

export const ItemLabel = styled.Text`
  color: ${({ theme }) => theme.colors.text};
  font-family: ${({ theme }) => theme.typography.fontFamily};
  text-transform: uppercase;
  font-size: ${({ theme }) => theme.typography.sizes.xs}px;
`
