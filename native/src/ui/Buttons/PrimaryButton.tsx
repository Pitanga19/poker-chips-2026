import styled from 'styled-components/native'

export const PrimaryButton = styled.TouchableOpacity`
  background-color: ${({ theme }) => theme.colors.buttonBackground};
  padding: ${({ theme }) => theme.spacing.md}px;
  border-radius: ${({ theme }) => theme.radii.md}px;
  align-items: center;
  justify-content: center;
`
