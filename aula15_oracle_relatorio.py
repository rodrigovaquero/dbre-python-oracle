import csv
import getpass
import os
import json
from pathlib import Path

import oracledb

def calcular_percentual(total, usado):
    return usado / total * 100

def classificar_status(percentual):
    if percentual >= 95:
        return "CRÍTICA"
    elif percentual >= 90:
        return "ALERTA"
    else:
        return "NORMAL"


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

            relatorio = []

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

                relatorio.append(
                     {
                    "tablespace": nome,
                    "total_gb": round(total_gb, 2),
                    "usado_gb": round(usado_gb, 2),
                    "percentual": round(percentual, 1),
                    "status": status
                     }
                )
                
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

            caminho_json = Path(
                "relatorio_oracle_tablespaces.json"
            )
            
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

            if (
                caminho_json.exists()
                and caminho_json.stat().st_size > 0
                and relatorio_validado == relatorio
            ):
                print(
                    f"JSON gerado: {caminho_json.resolve()} | "
                    f"Registros: {len(relatorio_validado)}"
                )
            else:
                raise SystemExit("ERRO: JSON não foi gerado ou validado corretamente.")    

            caminho_csv = Path(
                "relatorio_oracle_tablespaces.csv"
            )

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

            if (
                caminho_csv.exists()
                and caminho_csv.stat().st_size > 0
                and len(linhas_csv) == len(relatorio)
            ):
                print(
                    f"CSV gerado: {caminho_csv.resolve()} | "
                    f"Registros: {len(linhas_csv)}"
                )
            else:
                raise SystemExit(
                    "ERRO: CSV não foi gerado ou validado corretamente."
                )    
except oracledb.Error as erro:
    raise SystemExit(f"ERRO Oracle: {erro}") from erro