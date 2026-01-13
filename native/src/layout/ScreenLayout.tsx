import { Screen } from './Screen'
import { Background } from './Background'
import { AppLayout } from './AppLayout'
import { ScreenHeader } from '../ui/Header/ScreenHeader'

type Props = {
  children: React.ReactNode
  scroll?: boolean
  title?: string
  showBack?: boolean
  onBack?: () => void
}

export const ScreenLayout = ({
  children,
  scroll = false,
  title,
  showBack = false,
  onBack,
}: Props) => {
  return (
    <Screen>
      <Background source={require('../assets/background.png')} resizeMode='cover'>
        {title || showBack ? (
          <ScreenHeader
            title={title}
            showBack={showBack}
            onBack={onBack}
          />
        ) : null}
        
        <AppLayout scroll={scroll}>
          {children}
        </AppLayout>
      </Background>
    </Screen>
  )
}
