import { api } from './client'
import { GameStartResponse } from '../features/sessions/types'
import {
  LobbyCreateRequest,
  LobbyCreateResponse,
  LobbyJoinRequest,
  LobbyJoinResponse,
  GetLobbyResponse,
  LobbyUpdateRequest,
  LobbyUpdateResponse,
} from '../features/lobbies/types'

export const createLobby = async (payload: LobbyCreateRequest): Promise<LobbyCreateResponse> => {
  const { data } = await api.post('/lobbies', payload)
  return data
}

export const joinLobby = async (
  lobbyId: string, payload: LobbyJoinRequest
): Promise<LobbyJoinResponse> => {
  const { data } = await api.post(`/lobbies/${lobbyId}/join`, payload)
  return data
}

export const getLobby = async (lobbyId: string): Promise<GetLobbyResponse> => {
  const { data } = await api.get(`/lobbies/${lobbyId}`)
  return data
}

export const updateLobby = async (
  lobbyId: string, payload: LobbyUpdateRequest
): Promise<LobbyUpdateResponse> => {
  const { data } = await api.patch(`/lobbies/${lobbyId}`, payload)
  return data
}

export const deleteLobby = (lobbyId: string) =>
  api.delete(`/lobbies/${lobbyId}`)

export const startGameFromLobby = async (lobbyId: string): Promise<GameStartResponse> => {
  const { data } = await api.post(`/lobbies/${lobbyId}/start`)
  return data
}
