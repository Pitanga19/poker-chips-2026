from random import randint
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class UserData:
    id: int
    username: str

@dataclass
class LobbyPlayerState:
    id: int
    username: str
    position: int
    stack: int

@dataclass
class ToCreateLobbyData:
    lobby_id: str
    hoster_id: int
    hoster_username: str
    initial_stack: int
    self_position: int
    table_size: int
    big_blind_value: int

@dataclass
class GameSettings:
    hoster_id: int
    players: List[LobbyPlayerState]
    initial_stack: int
    table_size: int
    big_blind_value: int
    dealer_position: Optional[int] = None
    
    @property
    def small_blind_value(self) -> int:
        return self.big_blind_value // 2

@dataclass
class LobbyState:
    id: str
    settings: GameSettings
    
    @property
    def players_by_id(self) -> dict[int, LobbyPlayerState]:
        return {p.id: p for p in self.settings.players}
    
    @property
    def players_by_position(self) -> dict[int, LobbyPlayerState]:
        return {p.position: p for p in self.settings.players}
    
    @property
    def occupied_positions(self) -> List[int]:
        return [p.position for p in self.settings.players]
    
    @property
    def free_positions(self) -> List[int]:
        return [i for i in range(self.settings.table_size) if i not in self.occupied_positions]
    
    @property
    def random_free_position(self) -> int:
        return self.free_positions[randint(0, len(self.free_positions) - 1)]

@dataclass
class LobbyJoinResult:
    lobby: LobbyState
    player: LobbyPlayerState
