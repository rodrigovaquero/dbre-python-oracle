import csv
import json
from pathlib import Path


def gerar_json(relatorio, caminho):
    caminho_json = Path(caminho)

    with open(
        caminho_json,
        "w",
        encoding="utf-8"
    ) as arquivo:
        json.dump(
            relatorio,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

    with open(
        caminho_json,
        "r",
        encoding="utf-8"
    ) as arquivo:
        relatorio_validado = json.load(arquivo)

    if not (
        caminho_json.exists()
        and caminho_json.stat().st_size > 0
        and relatorio_validado == relatorio
    ):
        raise RuntimeError(
            "JSON não foi gerado ou validado corretamente."
        )

    return caminho_json

def gerar_csv(relatorio, caminho):
    caminho_csv = Path(caminho)

    with open(
        caminho_csv,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=[
                "tablespace",
                "total_gb",
                "usado_gb",
                "percentual",
                "status"
            ]
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

    if not (
        caminho_csv.exists()
        and caminho_csv.stat().st_size > 0
        and len(linhas_csv) == len(relatorio)
    ):
        raise RuntimeError(
            "CSV não foi gerado ou validado corretamente."
        )

    return caminho_csv