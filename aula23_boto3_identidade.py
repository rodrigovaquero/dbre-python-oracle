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
    cliente_sts = sessao.client(
    "sts",
    config=configuracao 
    )
    
    identidade = cliente_sts.get_caller_identity()

    print(f"Conta: {identidade['Account']}")
    print(f"Identidade: {identidade['Arn']}")
except (BotoCoreError, ClientError) as erro:
    raise SystemExit(f"ERRO AWS: {erro}") from erro