# Albion Market Analyzer

Aplicação em Python para coletar e armazenar preços do mercado de Albion Online.
O projeto usa PostgreSQL e futuramente ajudará a identificar oportunidades de lucro
entre cidades e o Black Market.

## Requisitos

- Windows
- Python 3.10
- PostgreSQL

## Como executar

No PowerShell, ative o ambiente virtual:

```powershell
.\venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz, usando `.env.example` como modelo, e configure
a variável `DATABASE_URL`. Não envie esse arquivo ao GitHub.

Na Discloud, o `.env` deve acompanhar os arquivos enviados no deploy. O
`discloud.config` já habilita a VLAN necessária para acessar o banco privado.

Crie as tabelas:

```powershell
python database.py
```

Consulte e salve os preços de 10 itens no Black Market:

```powershell
python main.py
```

Os preços são obtidos no servidor das Américas do Albion Online Data Project.
