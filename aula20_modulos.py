from dbre_calculos import calcular_percentual, classificar_status

percentual = calcular_percentual(500, 350)

status = classificar_status(percentual)

print(f"Utilização: {percentual:.1f}% | Status: {status}")    


