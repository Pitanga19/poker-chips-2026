import styled from 'styled-components/native'

export const Container = styled.View`
  flex: 1;
  justify-content: center;
  gap: ${({ theme }) => theme.spacing.lg}px;
`

export const DataContainer = styled.View`
  margin-top: ${({ theme }) => theme.spacing.xl}px;
  gap: ${({ theme }) => theme.spacing.md}px;
`
