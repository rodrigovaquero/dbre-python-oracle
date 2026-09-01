nome = "SYSTEM"
total_gb = 200
usado_gb = 190

percentual = usado_gb / total_gb * 100


if percentual >= 95:
    status = 'CRÍTICA'
elif percentual >= 90:
    status = 'ALERTA'    
else:    
    status = 'NORMAL'    


print(f"Tablespace: {nome} | Utilização: {percentual:.1f}% | Status: {status}")

