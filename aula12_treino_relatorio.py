import json

relatorio = []

tablespace_system = {
    "nome": "SYSTEM",
    "status": "CRÍTICA",
    "total_gb": 200
}

tablespace_users = {
    "nome": "USERS",
    "status": "NORMAL",
    "total_gb": 500
}

relatorio.append(tablespace_system)
relatorio.append(tablespace_users)


for tablespace in relatorio:
    
    print(f"Tablespace: {tablespace['nome']} | "
          f"Status: {tablespace['status']}")
    with open("relatorio_tablespaces.json", "w", encoding="utf-8") as arquivo:
        json.dump(relatorio, arquivo, ensure_ascii=False, indent=4)    

