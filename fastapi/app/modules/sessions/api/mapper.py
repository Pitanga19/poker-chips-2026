from typing import List, Optional
from uuid import UUID
from app.db.tables.hands.schemas import HandStreet
from app.modules.sessions.engine.managers.action_manager import ActionDescriptor
from app.modules.sessions.engine.managers.showdown_manager import (
    ShowdownPotInfo,
    ShowdownPotWinners,
    PayoutDescription,
)
from app.modules.sessions.api.schemas import (
    InGamePlayerInfo,
    ShowAvailableActions,
    GameStartRequest,
    GameStartResponse,
    GameRenderResponse,
    ActionDescriptorView,
    AvailableActionsResponse,
    BetRoundResultView,
    PotInfoView,
    LastActionView,
    PlayerActionResponse,
    ShowdownInfoResponse,
    PayoutDescriptionView,
    ShowdownResolveRequest,
    ShowdownResolveResponse,
)
from app.modules.sessions.engine.game_states import (
    PlayerState,
    PotState,
    BetRoundState,
    HandState,
    GameState,
)

class GameMapper:
    @staticmethod
    def _player_state_to_player_info(player: PlayerState) -> InGamePlayerInfo:
        return InGamePlayerInfo(
            id=player.id,
            username=player.username,
            position=player.position,
            stack=player.stack,
            betting_stack=player.betting_stack,
            is_active=player.is_active,
        )
    
    @staticmethod
    def request_to_game_state(request: GameStartRequest, game_id: UUID) -> GameState:
        table_size = request.table_size
        players = [
            PlayerState(
                id=p.id,
                username=p.username,
                position=p.position,
                stack=p.stack,
            )
            for p in request.players
        ]
        
        main_pot = PotState(
            size=0,
            players_in_pot=[p.id for p in players],
            pot_winners=[],
        )
        
        hand = HandState(
            street=HandStreet.PRE_FLOP,
            small_blind_value=request.small_blind_value,
            big_blind_value=request.big_blind_value,
            active_positions=[p.position for p in players],
            dealer_position=None,
        )
        
        bet_round = BetRoundState()
        
        return GameState(
            id=game_id,
            table_size=table_size,
            players=players,
            pots=[main_pot],
            hand=hand,
            bet_round=bet_round,
        )
    
    @staticmethod
    def game_state_to_start_response(
        gs: GameState,
        available_actions: ShowAvailableActions
    ) -> GameStartResponse:
        # Implementación para mapear GameState a GameStartResponse
        dealer = gs.players_by_position[gs.hand.dealer_position]
        small_blind = gs.players_by_position[gs.hand.small_blind_position]
        big_blind = gs.players_by_position[gs.hand.big_blind_position]
        pots = gs.pots
        
        return GameStartResponse(
            game_id=gs.id,
            table_size=gs.table_size,
            street=gs.hand.street,
            dealer_id=dealer.id,
            small_blind_id=small_blind.id,
            big_blind_id=big_blind.id,
            players=[
                GameMapper._player_state_to_player_info(player)
                for player in gs.players
            ],
            pots=[
                PotInfoView(
                    pot_index=i,
                    pot_size=pot.size,
                    players_in_pot=pot.players_in_pot,
                )
                for i, pot in enumerate(pots)
            ],
            available_actions=available_actions,
        )
    
    @staticmethod
    def game_state_to_render_response(gs: GameState) -> GameRenderResponse:
        # Implementación para mapear GameState a GameRenderResponse
        dealer = gs.players_by_position[gs.hand.dealer_position]
        small_blind = gs.players_by_position[gs.hand.small_blind_position]
        big_blind = gs.players_by_position[gs.hand.big_blind_position]
        current_player = gs.current_player
        pots = gs.pots
        
        last_turn = gs.last_turn
        last_acting_player = gs.players_by_id[last_turn.player_id] if last_turn else None
        
        return GameRenderResponse(
            game_id=gs.id,
            table_size=gs.table_size,
            street=gs.hand.street,
            dealer_id=dealer.id,
            small_blind_id=small_blind.id,
            big_blind_id=big_blind.id,
            current_player_id=current_player.id,
            players=[
                GameMapper._player_state_to_player_info(player)
                for player in gs.players
            ],
            pots=[
                PotInfoView(
                    pot_index=i,
                    pot_size=pot.size,
                    players_in_pot=pot.players_in_pot,
                )
                for i, pot in enumerate(pots)
            ],
            waiting_for_action=gs.current_player is not None,
            is_showdown=gs.hand.street == HandStreet.WINNER_SELECTION,
            last_action=LastActionView(
                player=GameMapper._player_state_to_player_info(last_acting_player),
                action=last_turn.action,
                amount=last_turn.amount,
            ) if last_turn else None
        )
    
    @staticmethod
    def request_to_available_actions_response(
        player: PlayerState,
        actions: List[ActionDescriptor],
    ) -> AvailableActionsResponse:
        player_info = GameMapper._player_state_to_player_info(player)
        
        actions_views = [
            ActionDescriptorView(
                type=action.type,
                min_amount=action.min_amount,
                max_amount=action.max_amount,
            )
            for action in actions
        ]
        
        return AvailableActionsResponse(
            player=player_info,
            actions=actions_views,
        )
    
    @staticmethod
    def request_to_player_action_response(
        game_state: GameState,
        bet_round_result: BetRoundResultView,
        next_available_actions: Optional[AvailableActionsResponse] = None,
    ) -> PlayerActionResponse:
        last_turn = game_state.last_turn
        acting_player = game_state.players_by_id[last_turn.player_id]
        player = GameMapper._player_state_to_player_info(acting_player)
        action = last_turn.action
        amount = last_turn.amount
        
        last_action = LastActionView(
            player=player,
            action=action,
            amount=amount,
        )
        
        pots = [
            PotInfoView(
                pot_index=i,
                pot_size=pot.size,
                players_in_pot=pot.players_in_pot,
            )
            for i, pot in enumerate(game_state.pots)
        ]
        return PlayerActionResponse(
            bet_round_result=bet_round_result,
            last_action=last_action,
            pots=pots,
            next_available_actions=next_available_actions,
        )
    
    @staticmethod
    def showdown_pots_info_to_response(pots_info: List[ShowdownPotInfo]) -> ShowdownInfoResponse:
        pots_to_resolve = [
            PotInfoView(
                pot_index=pot_info.pot_index,
                pot_size=pot_info.pot_size,
                players_in_pot=pot_info.players_in_pot,
            )
            for pot_info in pots_info
        ]
        
        return ShowdownInfoResponse(pots_to_resolve=pots_to_resolve)
    
    @staticmethod
    def request_to_showdown_pots_winners(
        request: ShowdownResolveRequest,
    ) -> List[ShowdownPotWinners]:
        pots_winners = [
            ShowdownPotWinners(
                pot_index=pot_winner.pot_index,
                pot_winners_ids=pot_winner.pot_winners_ids,
            )
            for pot_winner in request.pots_winners
        ]
        
        return pots_winners
    
    @staticmethod
    def payouts_to_showdown_resolve_response(payouts: List[PayoutDescription]) -> ShowdownResolveResponse:
        payouts_descriptions = [
            PayoutDescriptionView(
                player_id=payout.player_id,
                amount_won=payout.amount_won,
            )
            for payout in payouts
        ]
        
        return ShowdownResolveResponse(payout_descriptions=payouts_descriptions)
