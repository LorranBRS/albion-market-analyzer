from api_client import MarketAPIError, fetch_market_price
from database import create_database, save_market_price


def main() -> None:
    create_database()

    try:
        price = fetch_market_price("T4_BAG", "Caerleon")
    except MarketAPIError as error:
        print(f"Erro: {error}")
        return

    save_market_price(price)
    print(
        f"Preço salvo: {price['item_id']} em {price['city']} | "
        f"venda: {price['sell_price_min']} | compra: {price['buy_price_max']}"
    )


if __name__ == "__main__":
    main()
