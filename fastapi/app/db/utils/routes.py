import importlib
from pathlib import Path

def collect_db_routers() -> list:
    routers = []
    base_path = Path(__file__).resolve().parent.parent / 'tables'  # Va desde utils → db → tables
    
    for path in base_path.glob('*/routes.py'):  # Busca routes.py en subcarpetas de tables
        module_name = f'app.db.tables.{path.parent.name}.routes'  # Genera el nombre del módulo basado en la carpeta
        module = importlib.import_module(module_name)

        if hasattr(module, 'router'):
            routers.append(module.router)

    return routers