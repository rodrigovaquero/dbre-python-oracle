import json


try:
    with open("tablespaces_invalido.json", "r", encoding="utf-8") as arquivo:
        tablespaces = json.load(arquivo)

except FileNotFoundError as erro:
    print(f"ERRO: arquivo não encontrado | Detalhes: {erro}")

except json.JSONDecodeError as erro:
    print(f"ERRO: JSON inválido | Detalhes: {erro}")