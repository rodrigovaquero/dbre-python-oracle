import json

with open("relatorio_tablespaces.json", "r", encoding="utf-8") as arquivo:
    relatorio = json.load(arquivo)

for tablespace in relatorio:
    print(f"Tablespace: {tablespace['nome']} | "
          f"Status: {tablespace['status']}")
