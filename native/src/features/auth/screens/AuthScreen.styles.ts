import styled from 'styled-components/native'

export const Container = styled.View`
  flex: 1;
  justify-content: center;
  gap: ${({ theme }) => theme.spacing.lg}px;
`

export const SecondaryButtonContainer = styled.View`
  flex-direction: row;
  justify-content: space-between;
`