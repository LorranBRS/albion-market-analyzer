from database import create_database, list_tracked_items


def main() -> None:
    create_database()
    items = list_tracked_items()

    if not items:
        print("Nenhum item cadastrado.")
        return

    for item_id, item_name, enabled in items:
        status = "ativo" if enabled else "inativo"
        print(f"{item_id} - {item_name} ({status})")


if __name__ == "__main__":
    main()
