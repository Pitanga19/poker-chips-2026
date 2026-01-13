export enum ActionType {
  FOLD = 'fold',
  CALL = 'call',
  CHECK = 'check',
  BET = 'bet',
  RAISE = 'raise',
  ALL_IN = 'all_in',
}

export enum HandStreet {
  PRE_FLOP = 'pre-flop',
  FLOP = 'flop',
  TURN = 'turn',
  RIVER = 'river',
  WINNER_SELECTION = 'winner-selection',
  FINISHED = 'finished',
}

export enum BetRoundResult {
    NEXT_TURN = 'next-turn',
    FINISHED = 'finished',
}

export type ToCreatePlayerInfo = {
  id: number,
  username: string,
  position: number,
  stack: number,
}

export type InGamePlayerInfo = ToCreatePlayerInfo & {
  betting_stack: number,
  is_active: boolean,
}

export type PotInfoView = {
  pot_index: number,
  pot_size: number,
  players_in_pot: number[], // IDs de los jugadores en el pot
}

export type ActionDescriptorView = {
  type: ActionType,
  min_amount?: number,
  max_amount?: number,
}

export type ShowAvailableActions = {
  player: InGamePlayerInfo,
  actions: ActionDescriptorView[],
}

export type LastActionView = {
  player: InGamePlayerInfo,
  action: ActionType,
  amount?: number,
}

export type BetRoundResultView = {
  status: BetRoundResult,
  prev_street: HandStreet,
  new_street: HandStreet,
}

export type ShowdownPotWinnersView = {
  pot_index: number,
  pot_winners_ids: number[],
}

export type PayoutDescriptionView = {
  player_id: number,
  amount_won: number,
}

// Requests y Responses

export type GameStartRequest = {
  table_size: number,
  players: ToCreatePlayerInfo[],
  small_blind_value: number,
  big_blind_value: number,
  dealer_position?: number,
}

export type GameStartResponse = {
  game_id: string,
  table_size: number,
  street: HandStreet,
  dealer_id: number,
  small_blind_id: number,
  big_blind_id: number,
  players: InGamePlayerInfo[],
  pots: PotInfoView[],
  available_actions: ShowAvailableActions,
}

export type GameRenderResponse = GameStartResponse & {
  waiting_for_action: boolean,
  is_showdown: boolean,
  last_action?: LastActionView,
}

export type AvailableActionsResponse = ShowAvailableActions

export type PlayerActionRequest = {
  player_id: number,
  action: ActionType,
  amount?: number,
}

export type PlayerActionResponse = {
  bet_round_result: BetRoundResultView,
  last_action: LastActionView,
  pots: PotInfoView[],
  next_available_actions?: AvailableActionsResponse,
}

export type ShowdownInfoResponse = {
  pots_to_resolve: PotInfoView[],
}

export type ShowdownResolveRequest = {
  pots_winners: ShowdownPotWinnersView[],
}

export type ShowdownResolveResponse = {
  payout_descriptions: PayoutDescriptionView[],
}
