from app.modules.pre_game.gets.routes import router as gets_router
from app.modules.pre_game.management.routes import router as management_router
from app.modules.pre_game.player.routes import router as player_router

routers = [
    gets_router,
    management_router,
    player_router,
]