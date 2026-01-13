import { api } from './client'
import {
  GameStartRequest,
  GameStartResponse,
  GameRenderResponse,
  AvailableActionsResponse,
  PlayerActionRequest,
  PlayerActionResponse,
  ShowdownInfoResponse,
  ShowdownResolveRequest,
  ShowdownResolveResponse,
} from '../features/sessions/types'

export const startGameDirect = async (payload: GameStartRequest): Promise<GameStartResponse> => {
  const { data } = await api.post('/sessions', payload)
  return data
}

export const getGameState = async (gameId: string): Promise<GameRenderResponse> => {
  const { data } = await api.get(`/sessions/${gameId}/state`)
  return data
}

export const getAvailableActions = async (gameId: string):Promise<AvailableActionsResponse> => {
  const { data } = await api.get(`/sessions/${gameId}/actions`)
  return data
}

export const sendPlayerAction = async (
  gameId: string, payload: PlayerActionRequest
): Promise<PlayerActionResponse> => {
  const { data } = await api.post(`/sessions/${gameId}/actions`, payload)
  return data
}

export const getShowdownInfo = async (gameId: string): Promise<ShowdownInfoResponse> => {
  const { data } = await api.get(`/sessions/${gameId}/showdown`)
  return data
}

export const resolveShowdown = async (
  gameId: string, payload: ShowdownResolveRequest
): Promise<ShowdownResolveResponse> => {
  const { data } = await api.post(`/sessions/${gameId}/showdown`, payload)
  return data
}

export const nextHand = async (gameId: string): Promise<GameStartResponse> => {
  const { data } = await api.post(`/sessions/${gameId}/next-hand`)
  return data
}
