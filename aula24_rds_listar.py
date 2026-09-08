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
    total_oracle = 0
    total_disponiveis = 0

    for pagina in paginador.paginate():
        instancias = pagina["DBInstances"]
        total_instancias += len(instancias)

        for db_instance in instancias:
            if "oracle" in db_instance["Engine"]:
                total_oracle += 1
            if db_instance["DBInstanceStatus"] == "available":
                total_disponiveis += 1

    resumo = {
        "total_rds": total_instancias,
        "total_oracle": total_oracle,
        "total_disponiveis": total_disponiveis 
    }       
    

    print(F"Total de instâncias disponíveis: {total_disponiveis}")
    print(f"Total de instâncias RDS: {total_instancias}")
    print(f"Total de instâncias Oracle: {total_oracle}")
    print(f"Resumo: {resumo}")       

except (BotoCoreError, ClientError) as erro:
    raise SystemExit(f"ERRO AWS: {erro}") from erro