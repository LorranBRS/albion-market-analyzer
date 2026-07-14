from api_client import MarketAPIError, fetch_market_prices
from database import add_tracked_item, create_database, save_market_price


ITEMS = {
    "T4_BAG": "Bolsa do Adepto",
    "T4_CAPE": "Capa do Adepto",
    "T4_MAIN_SWORD": "Espada Larga do Adepto",
    "T4_2H_BOW": "Arco do Adepto",
    "T4_HEAD_PLATE_SET1": "Capacete de Soldado do Adepto",
    "T4_ARMOR_PLATE_SET1": "Armadura de Soldado do Adepto",
    "T4_SHOES_PLATE_SET1": "Botas de Soldado do Adepto",
    "T4_HEAD_LEATHER_SET1": "Capuz de Mercenário do Adepto",
    "T4_ARMOR_LEATHER_SET1": "Jaqueta de Mercenário do Adepto",
    "T4_SHOES_LEATHER_SET1": "Sapatos de Mercenário do Adepto",
}
CITY = "Black Market"


def main() -> None:
    create_database()

    for item_id, item_name in ITEMS.items():
        add_tracked_item(item_id, item_name)

    try:
        prices = fetch_market_prices(list(ITEMS), CITY)
    except MarketAPIError as error:
        print(f"Erro: {error}")
        return

    prices_by_item = {price["item_id"]: price for price in prices}

    print("\nPreços no Black Market:\n")
    print(
        f"{'ITEM':<28} {'COMPRA MIN':>12} {'COMPRA MAX':>12} "
        f"{'VENDA MIN':>12} {'VENDA MAX':>12}"
    )
    print("-" * 80)

    for item_id, item_name in ITEMS.items():
        price = prices_by_item.get(item_id)
        if price is None:
            print(f"{item_id:<28} {'sem dados':>51}")
            continue

        save_market_price(price)
        print(
            f"{item_id:<28} {price['buy_price_min']:>12} "
            f"{price['buy_price_max']:>12} {price['sell_price_min']:>12} "
            f"{price['sell_price_max']:>12}"
        )


if __name__ == "__main__":
    main()
