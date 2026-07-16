import os

from dotenv import load_dotenv
from supabase import Client, create_client


load_dotenv()


def get_supabase_client() -> Client:
    """Cria e retorna um cliente Supabase autenticado."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise RuntimeError(
            "As variáveis SUPABASE_URL e SUPABASE_KEY não foram configuradas. "
            "Crie um arquivo .env usando .env.example como modelo."
        )

    return create_client(url, key)


if __name__ == "__main__":
    client = get_supabase_client()
    print("Conexão com Supabase OK!")
    print(f"URL: {os.getenv('SUPABASE_URL')}")
