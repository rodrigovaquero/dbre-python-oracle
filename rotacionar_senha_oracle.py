import getpass
import os

import oracledb


dsn = os.getenv("ORACLE_DSN")
usuario = os.getenv("ORACLE_USER")

if dsn != "127.0.0.1:1521/ORCLPDB1":
    raise SystemExit(f"ERRO: destino não autorizado: {dsn}")

if usuario != "DBRE_MONITOR_LAB":
    raise SystemExit(f"ERRO: usuário não autorizado: {usuario}")

senha_atual = getpass.getpass("Senha atual: ")
senha_nova = getpass.getpass("Nova senha: ")
confirmacao = getpass.getpass("Confirme a nova senha: ")

if senha_nova != confirmacao:
    raise SystemExit("ERRO: as novas senhas são diferentes.")

if len(senha_nova) < 1:
    raise SystemExit("ERRO: a nova senha deve ter pelo menos 12 caracteres.")

try:
    with oracledb.connect(
        user=usuario,
        password=senha_atual,
        dsn=dsn,
        tcp_connect_timeout=5
    ) as connection:
        connection.changepassword(senha_atual, senha_nova)

    with oracledb.connect(
        user=usuario,
        password=senha_nova,
        dsn=dsn,
        tcp_connect_timeout=5
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT SYS_CONTEXT('USERENV', 'CURRENT_USER')
                FROM dual
                """
            )
            usuario_validado = cursor.fetchone()[0]

    print(f"Senha rotacionada e conexão validada: {usuario_validado}")

except oracledb.Error as erro:
    raise SystemExit(f"ERRO Oracle: {erro}") from erro