from uuid import UUID, uuid4
from app.core.exceptions import ValidationException
from app.db.tables.hands.schemas import HandStreet
from app.modules.sessions.engine.game_engine import GameEngine
from app.modules.sessions.engine.game_repository import GameRepository
from app.modules.sessions.engine.utils.enums import BetRoundResult
from app.modules.sessions.api.mapper import GameMapper
from app.modules.sessions.api.schemas import (
    BetRoundResultView,
    GameStartRequest,
    GameStartResponse,
    GameRenderResponse,
    AvailableActionsResponse,
    PlayerActionRequest,
    PlayerActionResponse,
    ShowdownInfoResponse,
    ShowdownResolveRequest,
    ShowdownResolveResponse,
)

class GameService:
    
    @staticmethod
    def start(request: GameStartRequest) -> GameStartResponse:
        """
        Inicia un nuevo juego con la configuración dada.
        """
        if request.table_size < len(request.players):
            raise ValidationException(
                'No hay suficientes asientos en la mesa para todos los jugadores.'
            )
        
        game_id = uuid4()
        game_state = GameMapper.request_to_game_state(request, game_id)
        
        engine = GameEngine(game_state)
        engine.start(dealer_position=request.dealer_position)
        GameRepository.save(engine.state)
        
        available_actions = GameService.available_actions(game_id)
        return GameMapper.game_state_to_start_response(engine.state, available_actions)
    
    @staticmethod
    def get_game_state(game_id: UUID) -> GameRenderResponse:
        """
        Obtiene el estado completo para renderizar un juego
        """
        game_state = GameRepository.get(game_id)
        
        return GameMapper.game_state_to_render_response(game_state)
    
    @staticmethod
    def available_actions(game_id: UUID) -> AvailableActionsResponse:
        """
        Obtiene las acciones disponibles para un jugador en una mano específica.
        """
        game_state = GameRepository.get(game_id)
        engine = GameEngine(game_state)
        player = engine.get_current_player()
        actions = engine.get_available_actions()
        
        return GameMapper.request_to_available_actions_response(player, actions)
    
    @staticmethod
    def player_action(game_id: UUID, request: PlayerActionRequest) -> PlayerActionResponse:
        """
        Procesa la acción de un jugador en una mano específica.
        """
        game_state = GameRepository.get(game_id)
        current_player = game_state.current_player
        
        # Verificar que se espere un jugador que actúe
        if current_player is None:
            raise ValidationException('Nadie debe actuar todavía!')
        
        # Verificar que sea el jugador que le toca actuar
        if request.player_id != current_player.id:
            raise ValidationException('No es tu turno de actuar!')
        
        engine = GameEngine(game_state)
        prev_street = engine.state.hand.street
        next_available_actions = None
        
        status = engine.action(request.action, request.amount)
        GameRepository.save(engine.state)
        
        if status == BetRoundResult.FINISHED:
            engine.handle_bet_round_finish()
            GameRepository.save(engine.state)
        
        new_street = engine.state.hand.street
        
        if new_street not in (HandStreet.WINNER_SELECTION, HandStreet.FINISHED):
            next_available_actions = GameService.available_actions(game_id)
        
        bet_round_result = BetRoundResultView(
            status=status,
            prev_street=prev_street,
            new_street=new_street,
        )
        
        return GameMapper.request_to_player_action_response(
            engine.state,
            bet_round_result,
            next_available_actions,
        )
    
    @staticmethod
    def get_showdown_info(game_id: UUID) -> ShowdownInfoResponse:
        """
        Obtiene la información necesaria para resolver el showdown de una mano específica.
        """
        game_state = GameRepository.get(game_id)
        engine = GameEngine(game_state)
        pots_info = engine.get_showdown_info()
        
        return GameMapper.showdown_pots_info_to_response(pots_info)
    
    @staticmethod
    def showdown_resolve(game_id: UUID, request: ShowdownResolveRequest) -> ShowdownResolveResponse:
        """
        Resuelve el showdown de una mano específica con los ganadores proporcionados.
        """
        game_state = GameRepository.get(game_id)
        engine = GameEngine(game_state)
        
        pots_winners = GameMapper.request_to_showdown_pots_winners(request)
        
        payouts = engine.showdown_resolve(pots_winners)
        GameRepository.save(engine.state)
        
        return GameMapper.payouts_to_showdown_resolve_response(payouts)
    
    @staticmethod
    def next_hand(game_id: UUID) -> GameStartResponse:
        """
        Inicia la siguiente mano de un juego específico.
        """
        game_state = GameRepository.get(game_id)
        engine = GameEngine(game_state)
        engine.next_hand()
        GameRepository.save(engine.state)
        
        return GameMapper.game_state_to_start_response(engine.state)
