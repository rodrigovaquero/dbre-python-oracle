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

    resposta = cliente_rds.describe_db_instances()

    instancias = resposta["DBInstances"]

    print(f"Instâncias RDS encontradas: {len(instancias)}")
        
except (BotoCoreError, ClientError) as erro:
    raise SystemExit(f"ERRO AWS: {erro}") from erro