from app.db.utils.routes import collect_db_routers
from app.modules.auth.routes import router as auth_router
from app.modules.pre_game.api import routers as pre_game_routers
from app.modules.in_game.api.routes import router as in_game_router

routers = collect_db_routers()
routers.append(auth_router)
routers.extend(pre_game_routers)
routers.append(in_game_router)
