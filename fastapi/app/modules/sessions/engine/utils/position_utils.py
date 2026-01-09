import random
from typing import List
from app.core.exceptions import ValidationException

def get_random_position(positions: List[int]) -> int:
    # Selecciona una posición aleatoria de la lista dada
    return random.choice(positions)

def get_next_position(current_position: int, position_list: List[int]) -> int:
    """
    Obtiene la siguiente posición en la lista circularmente
    
    - Si la posición actual es la última en la lista, retorna la primera posición
    - Si la posición actual no está en la lista, lanza una ValidationException
    """
    if current_position not in position_list:
        raise ValidationException('La posición actual no está en la lista de posiciones')
    
    current_index = position_list.index(current_position)
    next_index = (current_index + 1) % len(position_list)
    return position_list[next_index]
