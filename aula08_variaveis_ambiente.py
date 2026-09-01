import os   


banco = os.getenv("DBRE_BANCO")

if banco is None:
    raise SystemExit("ERRO: variável DBRE_BANCO não definida.")


print(f"Banco de Destino: {banco}")