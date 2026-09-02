from datetime import datetime, timezone   
from zoneinfo import ZoneInfo

data_execucao = datetime.now()

data_execucao_utc = datetime.now(timezone.utc)


data_sao_paulo = data_execucao_utc.astimezone(
    ZoneInfo("America/Sao_Paulo")
)

print(f"Data e hora em São Paulo: {data_sao_paulo.isoformat()}")

data_formatada = data_execucao.strftime("%d/%m/%Y %H:%M:%S")

print(f"Data e hora da execução: {data_formatada}")

ultima_coleta_texto = "2026-09-02 13:30:00"
try:
    ultima_coleta = datetime.strptime(
        ultima_coleta_texto,
        "%Y-%m-%d %H:%M:%S"
    )
except ValueError as erro:
    raise SystemExit(
        f"ERRO: data da última coleta inválida | Detalhes: {erro}"
    ) from erro

tempo_decorrido = data_execucao - ultima_coleta

minutos_decorridos = tempo_decorrido.total_seconds() / 60

if minutos_decorridos >= 60:
    status = "ATRASADA"
else:    
    status = "ATUAL"    

print (f"Status da coleta: {status}")


print(f"Minutos desde a última coleta: {minutos_decorridos:.1f}")


print(f"Data e hora em UTC: {data_execucao_utc.isoformat()}")