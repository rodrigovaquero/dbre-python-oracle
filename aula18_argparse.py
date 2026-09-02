import argparse

parser = argparse.ArgumentParser(
    description="Verificação de tablespaces Oracle"
)

parser.add_argument(
    "--limite-alerta",
    type=float,
    default=90,
    help="Percentual mínimo para gerar alerta"
)

parser.add_argument(
    "--limite-critico",
    type=float,
    default=95,
    help="Percentual mínimo para condição crítica"
)

args = parser.parse_args()

nome = "SYSAUX"
percentual = 92

if percentual >= args.limite_critico:
    status = "CRÍTICA"
elif percentual >= args.limite_alerta:
    status = "ALERTA"
else:
    status = "NORMAL"

print(
    f"Tablespace: {nome} | "
    f"Utilização: {percentual}% | "
    f"Status: {status}"
)