import styled from 'styled-components/native'

export const DisabledButton = styled.TouchableOpacity.attrs({
  activeOpacity: 1,
})`
  background-color: ${({ theme }) => theme.colors.buttonDisabledBackground};
  padding: ${({ theme }) => theme.spacing.md}px;
  border-radius: ${({ theme }) => theme.radii.md}px;
  align-items: center;
  justify-content: center;
`
