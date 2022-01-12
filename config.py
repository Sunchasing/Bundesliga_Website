from typing import Final


class DBConfig:

    host: Final[str] = 'localhost'
    port: Final[int] = 5432
    db_name: Final[str] = 'BundesligaDB'
    username: Final[str] = 'postgres'