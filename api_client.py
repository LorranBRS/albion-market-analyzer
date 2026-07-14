import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_BASE_URL = "https://west.albion-online-data.com"
REQUIRED_FIELDS = (
    "item_id",
    "city",
    "quality",
    "sell_price_min",
    "sell_price_min_date",
    "buy_price_max",
    "buy_price_max_date",
)


class MarketAPIError(Exception):
    """Erro ao consultar ou interpretar os dados de mercado."""


def fetch_market_price(
    item_id: str,
    city: str,
    quality: int = 1,
    timeout: int = 10,
) -> dict[str, object]:
    query = urlencode({"locations": city, "qualities": quality})
    url = f"{API_BASE_URL}/api/v2/stats/prices/{item_id}.json?{query}"
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "albion-market-analyzer/0.1",
        },
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            data = json.load(response)
    except HTTPError as error:
        raise MarketAPIError(f"A API respondeu com o erro HTTP {error.code}.") from error
    except (URLError, TimeoutError) as error:
        raise MarketAPIError("Não foi possível conectar à API de preços.") from error
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise MarketAPIError("A API retornou uma resposta inválida.") from error

    if not isinstance(data, list) or not data or not isinstance(data[0], dict):
        raise MarketAPIError("Nenhum preço foi encontrado para a consulta.")

    price = data[0]
    if any(field not in price for field in REQUIRED_FIELDS):
        raise MarketAPIError("A resposta da API não contém todos os campos esperados.")

    return {field: price[field] for field in REQUIRED_FIELDS}
