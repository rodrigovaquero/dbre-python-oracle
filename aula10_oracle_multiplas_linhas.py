import getpass
import os

import oracledb


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
                SELECT
                    tablespace_name,
                    status,
                    contents
                FROM dba_tablespaces
                ORDER BY tablespace_name
                """
            )

            resultados = cursor.fetchall()
            print(f"Linhas retornadas: {len(resultados)}")
            for nome, status, conteudo in resultados:
                print(
                    f"Tablespace: {nome} | "
                    f"Status: {status} | "
                    f"Conteúdo: {conteudo}"
                )

except oracledb.Error as erro:
    raise SystemExit(f"ERRO Oracle: {erro}") from erro