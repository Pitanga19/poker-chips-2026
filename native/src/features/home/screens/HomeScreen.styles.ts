import styled from 'styled-components/native'

export const Container = styled.View`
  flex: 1;
  justify-content: center;
  gap: ${({ theme }) => theme.spacing.lg}px;
`

export const LogoContainer = styled.View`
  align-items: center;
  justify-content: center;
  gap: ${({ theme }) => theme.spacing.md}px;
  height: 200px;
`

export const LogoImage = styled.Image`
  flex: 1;
  height: 100%;
  width: 100%;
`

export const Actions = styled.View`
  margin-top: ${({ theme }) => theme.spacing.xl}px;
  gap: ${({ theme }) => theme.spacing.md}px;
`
