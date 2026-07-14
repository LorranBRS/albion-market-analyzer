# Albion Market Analyzer

Aplicação em Python para coletar e armazenar preços do mercado de Albion Online.
O projeto usa SQLite e futuramente ajudará a identificar oportunidades de lucro
entre cidades e o Black Market.

## Requisitos

- Windows
- Python 3.10

## Como executar

No PowerShell, ative o ambiente virtual:

```powershell
.\venv\Scripts\Activate.ps1
```

Crie o banco de dados:

```powershell
python database.py
```

Liste os itens monitorados:

```powershell
python main.py
```

O banco é armazenado em `data/albion.db` e não é enviado ao GitHub.
