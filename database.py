import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "data" / "albion.db"


def create_database(database_path: Path = DATABASE_PATH) -> None:
    database_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(database_path) as connection:
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


def add_tracked_item(
    item_id: str,
    item_name: str,
    database_path: Path = DATABASE_PATH,
) -> bool:
    try:
        with sqlite3.connect(database_path) as connection:
            connection.execute(
                """
                INSERT INTO tracked_items (item_id, item_name)
                VALUES (?, ?)
                """,
                (item_id, item_name),
            )
    except sqlite3.IntegrityError:
        return False

    return True


def list_tracked_items(
    database_path: Path = DATABASE_PATH,
) -> list[tuple[str, str, bool]]:
    with sqlite3.connect(database_path) as connection:
        rows = connection.execute(
            """
            SELECT item_id, item_name, enabled
            FROM tracked_items
            ORDER BY item_name
            """
        ).fetchall()

    return [(item_id, item_name, bool(enabled)) for item_id, item_name, enabled in rows]


def set_item_enabled(
    item_id: str,
    enabled: bool,
    database_path: Path = DATABASE_PATH,
) -> bool:
    with sqlite3.connect(database_path) as connection:
        cursor = connection.execute(
            """
            UPDATE tracked_items
            SET enabled = ?
            WHERE item_id = ?
            """,
            (int(enabled), item_id),
        )

    return cursor.rowcount > 0


if __name__ == "__main__":
    create_database()
    print(f"Banco criado em: {DATABASE_PATH}")
