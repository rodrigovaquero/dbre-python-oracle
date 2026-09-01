def calcular_percentual(total_gb, usado_gb):
    percentual = usado_gb / total_gb * 100
    return percentual


def classificar_status(percentual):
    if percentual >= 95:
        return "CRÍTICA"
    elif percentual >= 90:
        return "ALERTA"
    else:
        return "NORMAL"

tablespaces = [
    {
     "nome": "SYSTEM",
     "total_gb": 200,
     "usado_gb": 190
    },
    {
     "nome": "USERS",
     "total_gb": 500,
     "usado_gb": 350
    },
    {
     "nome": "TEMP",
     "total_gb": 100,
     "usado_gb": 92
    }
]



for tablespace in tablespaces:

    percentual = calcular_percentual(
    tablespace["total_gb"],
    tablespace["usado_gb"]
    )
    
    status = classificar_status(percentual)

    print(
        f"Tablespace: {tablespace['nome']} | "
        f"Utilização: {percentual:.1f}% | "
        f"Status: {status}"
    )