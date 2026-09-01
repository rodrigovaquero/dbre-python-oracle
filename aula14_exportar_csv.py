import csv
import json
from pathlib import Path


with open("relatorio_tablespaces.json", "r", encoding="utf-8") as arquivo:
    relatorio = json.load(arquivo)

caminho_csv = Path("relatorio_tablespaces.csv")

with open(
    caminho_csv,
    "w",
    newline="",
    encoding="utf-8-sig"
) as arquivo:
    escritor = csv.DictWriter(
        arquivo,
        fieldnames=["nome", "total_gb", "status"]
    )
    escritor.writeheader()
    escritor.writerows(relatorio)

with open(
    caminho_csv,
    "r",
    newline="",
    encoding="utf-8-sig"
) as arquivo:
    leitor = csv.DictReader(arquivo)
    linhas_csv = list(leitor)

if (
    caminho_csv.exists()
    and caminho_csv.stat().st_size > 0
    and len(linhas_csv) == len(relatorio)
):
    print(
        f"CSV gerado e validado com sucesso: "
        f"{caminho_csv.resolve()} | "
        f"Registros: {len(linhas_csv)}"
    )
else:
    print(f"Falha ao gerar ou validar o CSV: {caminho_csv.resolve()}")


