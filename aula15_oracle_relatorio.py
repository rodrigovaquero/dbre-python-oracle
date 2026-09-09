
import argparse
import getpass
import os
import logging

import oracledb

from dbre.calculos import calcular_percentual, classificar_status
from dbre.relatorio import transformar_resultados
from dbre.arquivos import gerar_csv, gerar_json

def main():
    parser = argparse.ArgumentParser(
        description="Health check de tablespaces Oracle"
    )
    parser.add_argument(
        "--formato",
        choices=["json", "csv", "ambos"],
        default="ambos",
        help="Formato do relatório gerado"
)
    argumentos = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    logging.info("Iniciando health check de tablespaces Oracle.")

    dsn = os.getenv("ORACLE_DSN")
    usuario = os.getenv("ORACLE_USER")
    senha = os.getenv("ORACLE_PASSWORD")

    if senha is None:
        senha = getpass.getpass("Senha Oracle: ")

    if not dsn or not usuario or not senha:
        raise SystemExit("ERRO: configuração Oracle incompleta.")

    try:
        with oracledb.connect(
            user=usuario,
            password=senha,
            dsn=dsn,
            tcp_connect_timeout=5
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    select
                    df.tablespace_name,
    df.total_bytes,
    df.total_bytes - NVL(fs.free_bytes, 0) AS usado_bytes,
    df.max_bytes,
    df.total_arquivos,
    df.arquivos_autoextend
    FROM (
        SELECT
            tablespace_name,
            SUM(bytes) AS total_bytes,
            COUNT(*) AS total_arquivos,
            SUM(
                CASE
                    WHEN autoextensible = 'YES' THEN maxbytes
                    ELSE bytes
                END
            ) AS max_bytes,
            SUM(
                CASE
                    WHEN autoextensible = 'YES' THEN 1
                    ELSE 0
                END
            ) AS arquivos_autoextend
        FROM dba_data_files
        GROUP BY tablespace_name
    ) df
    LEFT JOIN (
        SELECT
            tablespace_name,
            SUM(bytes) AS free_bytes
        FROM dba_free_space
        GROUP BY tablespace_name
    ) fs
        ON fs.tablespace_name = df.tablespace_name
    ORDER BY df.tablespace_name
                    """
                )

                resultados = cursor.fetchall()

                relatorio = transformar_resultados(resultados)

                for (
                    nome,
                    total_bytes,
                    usado_bytes,
                    max_bytes,
                    total_arquivos,
                    arquivos_autoextend
                ) in resultados:
                    total_gb = total_bytes / 1024 ** 3
                    usado_gb = usado_bytes / 1024 ** 3
                    max_gb = max_bytes / 1024 ** 3

                    percentual = calcular_percentual(
                        total_bytes,
                        usado_bytes
                    )

                    percentual_maximo = calcular_percentual(
                        max_bytes,
                        usado_bytes
                    )

                    status = classificar_status(percentual)

                                
                    print(
                        f"Tablespace: {nome} | "
                        f"Alocado: {total_gb:.2f} GB | "
                        f"Limite: {max_gb:.2f} GB | "
                        f"Usado: {usado_gb:.2f} GB | "
                        f"Uso alocado: {percentual:.1f}% | "
                        f"Uso do limite: {percentual_maximo:.4f}% | "
                        f"Autoextend: {arquivos_autoextend}/{total_arquivos} datafiles | "
                        f"Status atual: {status}"
                    )
                print(relatorio)

                if argumentos.formato in ("json", "ambos"):
                    caminho_json = gerar_json(
                        relatorio,
                        "relatorio_oracle_tablespaces.json"
                    )

                    print(
                        f"JSON gerado: {caminho_json.resolve()} | "
                        f"Registros: {len(relatorio)}"
                    )   

                if argumentos.formato in ("csv", "ambos"):
                    caminho_csv = gerar_csv(
                        relatorio,
                        "relatorio_oracle_tablespaces.csv"
                    )

                    print(
                        f"CSV gerado: {caminho_csv.resolve()} | "
                        f"Registros: {len(relatorio)}"
                    )

        logging.info(
            f"Health check concluído. Registros: {len(relatorio)}"
        )

    except oracledb.Error as erro:
        logging.error(f"Falha na consulta Oracle: {erro}")
        raise SystemExit(1) from erro

if __name__ == "__main__":
    main()    