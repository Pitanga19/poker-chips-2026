export enum AuthActionType {
  REGISTER = 'register',
  LOGIN = 'login',
  LOGOUT = 'logout',
}

export type AuthAction = {
  type: AuthActionType,
  payload?: AuthResponse,
}

export type UserRead = {
  id: number,
  username: string,
}

export type AuthLoginData = {
  username: string,
  password: string,
}

export type AuthRegisterData = AuthLoginData & {
  password_confirm: string,
}

export type Token = {
  access_token: string,
  token_type: string,
}

export type TokenData = {
  id: number,
  username: string,
}

export type AuthResponse = {
  token: Token,
  user: TokenData,
}

export type AuthState = {
  token: Token | null,
  user: TokenData | null,
  isAuthenticated: boolean,
}
