import sqlite3
from pathlib import Path


BASE_DIR = Path(file).resolve().parent
DATABASE_PATH = BASE_DIR / "data" / "albion.db"


def create_database() -> None:
    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS tracked_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id TEXT NOT NULL UNIQUE,
            item_name TEXT NOT NULL,
            enabled INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()
    connection.close()

    print(f"Banco criado em: {DATABASE_PATH}")


if name == "main":
    create_database()