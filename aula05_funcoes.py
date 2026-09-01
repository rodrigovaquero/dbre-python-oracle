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


percentual = calcular_percentual(500, 350)
status = classificar_status(percentual)

print(f"Utilização: {percentual:.1f}% | Status: {status}")