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
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS market_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id TEXT NOT NULL,
                city TEXT NOT NULL,
                quality INTEGER NOT NULL,
                sell_price_min INTEGER NOT NULL,
                sell_price_min_date TEXT NOT NULL,
                sell_price_max INTEGER NOT NULL,
                sell_price_max_date TEXT NOT NULL,
                buy_price_min INTEGER NOT NULL,
                buy_price_min_date TEXT NOT NULL,
                buy_price_max INTEGER NOT NULL,
                buy_price_max_date TEXT NOT NULL,
                fetched_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (item_id, city, quality)
            )
            """
        )

        existing_columns = {
            row[1]
            for row in connection.execute("PRAGMA table_info(market_prices)").fetchall()
        }
        missing_columns = {
            "sell_price_max": "INTEGER NOT NULL DEFAULT 0",
            "sell_price_max_date": "TEXT NOT NULL DEFAULT ''",
            "buy_price_min": "INTEGER NOT NULL DEFAULT 0",
            "buy_price_min_date": "TEXT NOT NULL DEFAULT ''",
        }

        for column_name, column_definition in missing_columns.items():
            if column_name not in existing_columns:
                connection.execute(
                    f"ALTER TABLE market_prices "
                    f"ADD COLUMN {column_name} {column_definition}"
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


def save_market_price(
    price: dict[str, object],
    database_path: Path = DATABASE_PATH,
) -> None:
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            """
            INSERT INTO market_prices (
                item_id,
                city,
                quality,
                sell_price_min,
                sell_price_min_date,
                sell_price_max,
                sell_price_max_date,
                buy_price_min,
                buy_price_min_date,
                buy_price_max,
                buy_price_max_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (item_id, city, quality) DO UPDATE SET
                sell_price_min = excluded.sell_price_min,
                sell_price_min_date = excluded.sell_price_min_date,
                sell_price_max = excluded.sell_price_max,
                sell_price_max_date = excluded.sell_price_max_date,
                buy_price_min = excluded.buy_price_min,
                buy_price_min_date = excluded.buy_price_min_date,
                buy_price_max = excluded.buy_price_max,
                buy_price_max_date = excluded.buy_price_max_date,
                fetched_at = CURRENT_TIMESTAMP
            """,
            (
                price["item_id"],
                price["city"],
                price["quality"],
                price["sell_price_min"],
                price["sell_price_min_date"],
                price["sell_price_max"],
                price["sell_price_max_date"],
                price["buy_price_min"],
                price["buy_price_min_date"],
                price["buy_price_max"],
                price["buy_price_max_date"],
            ),
        )


if __name__ == "__main__":
    create_database()
    print(f"Banco criado em: {DATABASE_PATH}")
