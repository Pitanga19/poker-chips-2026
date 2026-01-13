export type UserInfo = {
  id: number,
  username: string,
}

export type LobbyPlayerInfo = UserInfo & {
  position: number,
  stack: number,
}

export type LobbyFullData = {
  lobby_id: string,
  hoster_id: number,
  players: LobbyPlayerInfo[],
  initial_stack: number,
  table_size: number,
  small_blind_value: number,
  big_blind_value: number,
  dealer_position?: number,
}

// Requests y Responses

export type LobbyCreateRequest = {
  hoster_info: UserInfo,
  table_size: number,
  big_blind_value: number,
  initial_stack: number,
  self_position?: number,
}

export type LobbyCreateResponse = LobbyFullData

export type LobbyJoinRequest = {
  user: UserInfo,
}

export type LobbyJoinResponse = LobbyFullData & {
  joined_player: LobbyPlayerInfo
}

export type GetLobbyResponse = LobbyFullData

export type LobbyUpdateRequest = {
  table_size?: number,
  big_blind_value?: number,
  initial_stack?: number,
  dealer_position?: number,
}

export type LobbyUpdateResponse = LobbyFullData
