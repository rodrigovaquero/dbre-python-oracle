import boto3

sessao = boto3.Session(
    region_name="us-east-1"
)

print(f"Região configurada: {sessao.region_name}")
print(f"Profiles encontrados: {sessao.available_profiles}")