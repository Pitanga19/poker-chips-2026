import React from 'react'
import styled from 'styled-components/native'
import { useTheme } from 'styled-components/native'
import { IconButton } from '../Buttons/IconButton'

const Container = styled.View`
  height: 56px;
  flex-direction: row;
  align-items: center;
  padding-horizontal: ${({ theme }) => theme.spacing.md}px;
`

const Left = styled.View`
  width: 40px;
  align-items: flex-start;
`

const Center = styled.View`
  flex: 1;
  align-items: center;
`

const Right = styled.View`
  width: 40px;
`

const Title = styled.Text`
  font-size: ${({ theme }) => theme.typography.sizes.lg}px;
  font-weight: ${({ theme }) => theme.typography.weights.medium};
  color: ${({ theme }) => theme.colors.text};
`

type Props = {
  title?: string
  showBack?: boolean
  onBack?: () => void
}

export const ScreenHeader = ({
  title,
  showBack = false,
  onBack,
}: Props) => {
  const theme = useTheme()

  return (
    <Container>
      <Left>
        {showBack && (
          <IconButton
            icon='chevron-back'
            onPress={onBack}
            color={theme.colors.text}
          />
        )}
      </Left>
      
      <Center>
        {title && <Title>{title}</Title>}
      </Center>
      
      <Right />
    </Container>
  )
}
