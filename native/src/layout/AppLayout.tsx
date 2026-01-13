import { ReactNode } from 'react'
import styled, { css } from 'styled-components/native'

const Base = css`
  flex: 1;
  padding: ${({ theme }) => theme.spacing.md}px;
`

const ViewContainer = styled.View`
  ${Base}
`

const ScrollContainer = styled.ScrollView.attrs({
  contentContainerStyle: {
    flexGrow: 1,
  },
})`
  ${Base}
`

type Props = {
  children: ReactNode
  scroll?: boolean
}

export const AppLayout = ({ children, scroll = false }: Props) => {
  if (scroll) return <ScrollContainer>{children}</ScrollContainer>
  return <ViewContainer>{children}</ViewContainer>
}
