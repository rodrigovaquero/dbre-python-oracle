import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

def criar_resumo(total_instancias, total_oracle, total_disponiveis):
    return {
        "total_rds": total_instancias,
        "total_oracle": total_oracle,
        "total_disponiveis": total_disponiveis
    }

def eh_oracle(db_instance):
    return "oracle" in db_instance["Engine"]

def esta_disponivel(db_instance):
    return db_instance["DBInstanceStatus"] == "available"

def criar_paginador_rds(sessao, configuracao, regiao):
    cliente_rds = sessao.client(
        "rds",
        region_name=regiao,
        config=configuracao
    )

    return cliente_rds.get_paginator(
        "describe_db_instances"
    )

def contar_instancias(paginador):
    total_instancias = 0
    total_oracle = 0
    total_disponiveis = 0

    for pagina in paginador.paginate():
        instancias = pagina["DBInstances"]
        total_instancias += len(instancias)

        for db_instance in instancias:
            if eh_oracle(db_instance):
                total_oracle += 1

            if esta_disponivel(db_instance):
                total_disponiveis += 1

    return criar_resumo(
        total_instancias,
        total_oracle,
        total_disponiveis
    )

def main():
        
    configuracao = Config(
        connect_timeout=5,
        read_timeout=10
    )

    regioes = [
        "us-east-1",
        "sa-east-1"
    ]

    sessao = boto3.Session(
        profile_name="dbre-lab",
        region_name="us-east-1"  
    )

    total_geral = 0

    for regiao in regioes:
        print(f"Região que será consultada: {regiao}")

        try:
            paginador = criar_paginador_rds(
                sessao,
                configuracao,
                regiao
            )

            resumo = contar_instancias(paginador)

            total_instancias = resumo["total_rds"]
            total_oracle = resumo["total_oracle"]
            total_disponiveis = resumo["total_disponiveis"]

            total_geral += total_instancias

            print(f"Total de instâncias disponíveis: {total_disponiveis}")
            print(f"Total de instâncias RDS: {total_instancias}")
            print(f"Total de instâncias Oracle: {total_oracle}")
            print(f"Resumo: {resumo}")

        except (BotoCoreError, ClientError) as erro:
            raise SystemExit(f"ERRO AWS: {erro}") from erro
    print(f"Total geral em todas as regiões: {total_geral}")

if __name__ == "__main__":
    main()    