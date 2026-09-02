resposta = {
    "DBInstances": [
        {
            "DBInstanceIdentifier": "oracle-lab-01",
            "Engine": "oracle-se2",
            "DBInstanceStatus": "available",
            "AllocatedStorage": 500,
            "MultiAZ": False
        },
        {
            "DBInstanceIdentifier": "postgres-lab-01",
            "Engine": "postgres",
            "DBInstanceStatus": "stopped",
            "AllocatedStorage": 100,
            "MultiAZ": False
        }
    ]
}
instancias = resposta["DBInstances"]

inventario_oracle = []

for db_instance in instancias:
    if db_instance["Engine"].startswith("oracle"):
        print(f"ID: {db_instance['DBInstanceIdentifier']}")
        print(f"Engine: {db_instance['Engine']}")
        print(f"Status: {db_instance['DBInstanceStatus']}")
        print(f"Storage: {db_instance['AllocatedStorage']} GB")
        if not db_instance["MultiAZ"]:
            status_multiaz = "ALERTA: SEM MULTI-AZ"
        else:
            status_multiaz = "Protegida"
        print(f"Status MultiAZ: {status_multiaz}")  

        registro = {
            "identificador": db_instance["DBInstanceIdentifier"],
            "engine": db_instance["Engine"],
            "storage_gb": db_instance["AllocatedStorage"],
            "multi_az": db_instance["MultiAZ"],
            "status_multiaz": status_multiaz
        }
        inventario_oracle.append(registro)

print(inventario_oracle)        


     

       