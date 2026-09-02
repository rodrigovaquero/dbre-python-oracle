import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError


configuracao = Config(
    connect_timeout=5,
    read_timeout=10
)

sessao = boto3.Session(
    profile_name="dbre-lab",
    region_name="us-east-1"
)

cliente_sts = sessao.client(
    "sts",
    config=configuracao
)

try:
    cliente_rds = sessao.client(
    "rds",
    config=configuracao
    )

    paginador = cliente_rds.get_paginator(
    "describe_db_instances"
    )

    total_instancias = 0

    for pagina in paginador.paginate():
        instancias = pagina["DBInstances"]
        total_instancias += len(instancias)

    print(f"Total de instâncias RDS: {total_instancias}")
        
except (BotoCoreError, ClientError) as erro:
    raise SystemExit(f"ERRO AWS: {erro}") from erro