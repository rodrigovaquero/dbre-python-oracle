import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logging.info("Iniciando verificação de tablespaces.")

nome = "SYSAUX"
percentual = 92

if percentual >= 95:
    logging.error(f"Tablespace {nome} com utilização de {percentual}%.")
elif percentual >= 90:
    logging.warning(f"Tablespace {nome} com utilização de {percentual}%.")
else:
    logging.info(f"Tablespace {nome} com utilização dentro do limite: {percentual}%.")