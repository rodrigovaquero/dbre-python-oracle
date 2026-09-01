import os

import oracledb


dsn = os.getenv("ORACLE_DSN")
usuario = os.getenv("ORACLE_USER")
senha = os.getenv("ORACLE_PASSWORD")

if not dsn or not usuario or not senha:
    raise SystemExit("ERRO: configuração Oracle incompleta.")
try:
    with oracledb.connect(
        user=usuario,
        password=senha,
        dsn=dsn,
        tcp_connect_timeout=5
    ) as connection:
        print(
            f"Conexão realizada | "
            f"Destino: {dsn} | "
            f"Usuário: {usuario} | "
            f"Versão: {connection.version}"
        )

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    SYS_CONTEXT('USERENV', 'DB_NAME'),
                    SYS_CONTEXT('USERENV', 'SERVICE_NAME'),
                    SYS_CONTEXT('USERENV', 'CURRENT_USER')
                FROM dual
                """
            )

            db_name, service_name, current_user = cursor.fetchone()

            print(
                f"Banco: {db_name} | "
                f"Serviço: {service_name} | "
                f"Usuário: {current_user}"
            )

except oracledb.Error as erro:
    raise SystemExit(f"ERRO Oracle: {erro}") from erro