from .db_manager import DBManager, DatabaseConfig
from config import config

# Initialize singleton here
db_manager = DBManager(
    db_config=DatabaseConfig(kind="supabase", dsn=config.POSTGRES_DSN),
)

__all__ = ["db_manager", "DBManager", "DatabaseConfig"]
