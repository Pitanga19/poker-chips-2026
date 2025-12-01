from typing import Optional
from app.core.exceptions import ValidationException
from app.db.utils import crud_helper as helper
from app.db.utils.base_crud import BaseCRUD
from app.db.tables.room_settings.model import RoomSettings
from app.db.tables.room_settings.schemas import RoomSettingsCreate, RoomSettingsOptional
from app.db.tables.rooms.model import Room

class RoomSettingsCRUD(BaseCRUD[RoomSettings, RoomSettingsCreate, RoomSettingsOptional]):    
    async def validate_create(self, data: RoomSettingsCreate, db):
        # Verificar que exista la room
        await helper.get_validated(
            stmt=Room.__table__.select().filter_by(id=data.room_id),
            should_exist=True,
            search_fields=[helper.SearchField(field='id', value=data.room_id)],
            db=db
        )

        # Verificar que no exista otra configuración para esta room
        existing = await self.get_filtered(
            search_fields=[helper.SearchField(field='room_id', value=data.room_id)],
            db=db
        )
        if len(existing) > 0:
            raise ValidationException(
                f'La sala con id {data.room_id} ya tiene settings configurados'
            )
        
        # Calcular valor de small_blind_value
        data.small_blind_value = data.big_blind_value // 2

        # Aplicar validaciones
        self._validate_buy_in_logic(data.use_default_buy_in, data.buy_in)
        self._validate_blinds_values(data.small_blind_value, data.big_blind_value)
        self._validate_stack(data.min_stack_bb, data.max_stack_bb)

    async def validate_update(self, id: int, data: RoomSettingsOptional, db):
        # Obtener settings actual
        settings = await self.get_by_id(id, db)

        # Evitar modificar room_id
        if data.room_id is not None:
            raise ValidationException('No se puede modificar room_id de una configuración')

        # Evitar modificar small_blind_value directamente
        if data.small_blind_value is not None:
            raise ValidationException('No se puede modificar la small_blind_value directamente')

        # Resolver valores finales (mezcla de actuales + enviados)
        use_default = (
            data.use_default_buy_in
            if data.use_default_buy_in is not None
            else settings.use_default_buy_in
        )

        buy_in_value = (
            data.buy_in
            if data.buy_in is not None
            else settings.buy_in
        )
        
        # Eliminar buy_in si corresponde
        if use_default is False:
            data.buy_in = None
            buy_in_value = None
        
        big = data.big_blind_value if data.big_blind_value is not None else settings.big_blind_value
        small = big // 2
        data.small_blind_value = small

        min_stack = data.min_stack_bb if data.min_stack_bb is not None else settings.min_stack_bb
        max_stack = data.max_stack_bb if data.max_stack_bb is not None else settings.max_stack_bb

        # Aplicar validaciones
        self._validate_buy_in_logic(use_default, buy_in_value)
        self._validate_blinds_values(small, big)
        self._validate_stack(min_stack, max_stack)

    # Verificar coherencia de buy-in
    def _validate_buy_in_logic(self, use_default: bool, buy_in: Optional[int]):
        if use_default is True:
        # Caso: usar valor por defecto → buy_in → obligatorio y > 0
            if buy_in is None:
                raise ValidationException(
                    'Debe especificarse un buy_in al activar use_default_buy_in'
                )
            if buy_in <= 0:
                raise ValidationException('buy_in debe ser mayor a 0')
        else:
            # Sin use_default → buy_in debe ser None
            if buy_in is not None:
                raise ValidationException(
                    'No puede especificarse buy_in si se desactiva use_default_buy_in'
                )
    
        # Verificar valores de ciegas
    def _validate_blinds_values(self, small: int | None, big: int | None):
        if small is not None:
            if small <= 0:
                raise ValidationException('small_blind_value debe ser mayor que 0')

        if big is not None:
            if big < 2:
                raise ValidationException('big_blind_value debe ser mayor o igual a 2')

        if small is not None and big is not None:
            if big <= small:
                raise ValidationException('big_blind_value debe ser mayor que small_blind_value')

    # Verificar consistencia de min/max stack
    def _validate_stack(self, min_stack: int | None, max_stack: int | None):
        if min_stack is not None and min_stack <= 0:
            raise ValidationException('min_stack_bb debe ser mayor que 0')

        if max_stack is not None and max_stack <= 0:
            raise ValidationException('max_stack_bb debe ser mayor que 0')

        if min_stack is not None and max_stack is not None:
            if min_stack > max_stack:
                raise ValidationException('max_stack_bb debe ser mayor o igual que min_stack_bb')

room_settings_crud = RoomSettingsCRUD(
    model=RoomSettings,
    schema_create=RoomSettingsCreate,
    schema_update=RoomSettingsOptional
)
