from typing import Optional, List
from app.db.tables.hands.schemas import HandStreet
from app.modules.in_game.engine.game_states import GameState, PlayerState
from app.modules.in_game.engine.flow.hand_flow import HandFlow
from app.modules.in_game.engine.flow.bet_round_flow import BetRoundFlow
from app.modules.in_game.engine.utils.enums import BetRoundResult, HandResult
from app.modules.in_game.engine.managers.pot_manager import PayoutDescription
from app.modules.in_game.engine.utils.street_utils import advance_hand_street
from app.modules.in_game.engine.managers.action_manager import (
    ActionManager,
    ActionType,
    ActionDescriptor,
)
from app.modules.in_game.engine.managers.showdown_manager import (
    ShowdownManager,
    ShowdownPotWinners,
    ShowdownPotInfo,
)

class GameEngine:
    def __init__(self, game_state: GameState):
        self.state = game_state
    
    def get_current_player(self) -> PlayerState:
        return self.state.current_player
    
    # HAND LIFECYCLE
    def start(self, dealer_position: Optional[int] = None) -> None:
        """Inicia una nueva mano"""
        HandFlow.start(self.state, dealer_position)
    
    def next_hand(self) -> None:
        """
        Inicia la siguiente mano
        Se asume que la mano actual ya fue finalizada
        """
        HandFlow.start(self.state)
    
    # PLAYER ACTIONS
    def get_available_actions(self) -> List[ActionDescriptor]:
        return ActionManager.get_available_actions(self.state)
    
    def action(self, action: ActionType, amount: Optional[int] = None) -> BetRoundResult:
        """
        Ejecuta una acción del jugador actual y orquesta el flujo correspondiente
        """
        return BetRoundFlow.after_action(self.state, action, amount)
    
    # BET ROUND / HAND FLOW
    def handle_bet_round_finish(self) -> None:
        BetRoundFlow.finish(self.state)
        hand_result = HandFlow.after_bet_round(self.state)
        
        match hand_result:
            case HandResult.NEXT_STREET:
                self._next_street()
            
            case HandResult.SHOWDOWN:
                HandFlow.finish(self.state)
            
            case HandResult.AUTO_WIN:
                HandFlow.finish(self.state)
    
    def _next_street(self) -> None:
        advance_hand_street(self.state.hand)
        BetRoundFlow.start(self.state)
    
    # SHOWDOWN
    def get_showdown_info(self) -> List[ShowdownPotInfo]:
        return ShowdownManager.get_showdown_info(self.state)
    
    def showdown_resolve(
        self,
        pots_winners: List[ShowdownPotWinners],
    ) -> List[PayoutDescription]:
        """
        Resolver showdown interactivo.
        Luego de esto, la mano queda finalizada
        y se puede llamar a next_hand().
        """
        payout_descriptions = ShowdownManager.resolve(self.state, pots_winners)
        
        # Marcar mano como finalizada
        self.state.hand.street = HandStreet.FINISHED
        
        return payout_descriptions
