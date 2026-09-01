def calcular_percentual(total, usado):
    return usado / total * 100

def classificar_status(percentual):
    if percentual >= 95:
        return "CRÍTICA"
    elif percentual >= 90:
        return "ALERTA"
    else:
        return "NORMAL"
    