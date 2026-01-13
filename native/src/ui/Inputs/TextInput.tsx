import styled from 'styled-components/native'

export const TextInput = styled.TextInput`
  border-width: 1px;
  background: ${({ theme }) => theme.colors.inputBackground};
  padding: ${({ theme }) => theme.spacing.md}px;
  border-radius: ${({ theme }) => theme.radii.md}px;
  color: ${({ theme }) => theme.colors.text};
`
