from app.db.utils.routes import collect_db_routers
from app.modules.auth.routes import router as auth_router
from app.modules.pre_game.api import routers as pre_game_routers
from app.modules.lobbies.api.routes import router as lobbies_router
from app.modules.sessions.api.routes import router as sessions_router

routers = collect_db_routers()
routers.append(auth_router)
routers.extend(pre_game_routers)
routers.append(lobbies_router)
routers.append(sessions_router)
