import boto3

resposta = {
    "DBInstances": [
        {
            "DBInstanceIdentifier": "oracle-producao-01",
            "Engine": "oracle-se2",
            "DBInstanceStatus": "available",
            "AllocatedStorage": 500,
            "MultiAZ": True
        },
        {
            "DBInstanceIdentifier": "postgres-homologacao-01",
            "Engine": "postgres",
            "DBInstanceStatus": "stopped",
            "AllocatedStorage": 100,
            "MultiAZ": False
        },
        {
            "DBInstanceIdentifier": "oracle-desenvolvimento-01",
            "Engine": "oracle-ee",
            "DBInstanceStatus": "available",
            "AllocatedStorage": 200,
            "MultiAZ": False
        }
    ],
    "ResponseMetadata": {
        "HTTPStatusCode": 200
    }
}


instancias = resposta["DBInstances"] # atribui à  variavel instancias o valor da chave DBInstances 
print(instancias)
quantidade_elementos = len(instancias)
print(quantidade_elementos)

#Percorra a lista instancias e imprima um dicionário por vez.

instancias_oracle = []

total_disponiveis = 0

for db_instance  in instancias:
    if db_instance["Engine"].startswith("oracle"): #se o valor da chave Engine começar com oracle
        instancias_oracle.append(db_instance) #adicionando as Engines que começarem com oracle na lista instancias_oracle
        print(db_instance["DBInstanceIdentifier"]) #imprima o valor da chave DBInstanceIdentifier
    if db_instance["DBInstanceStatus"] == "available": #se o valor da chave DBInstanceStatus for igual a available
        total_disponiveis += 1 #incrementa a variável total_disponiveis em 1


resumo = {
    "TotalInstancias": len(instancias),
    "Total_Oracle": len(instancias_oracle),
    "TotalInstanciasDisponiveis": total_disponiveis,
    "Codigo_Http": resposta["ResponseMetadata"]["HTTPStatusCode"]
}

print(resumo) #imprima o dicionário resumo
print (f"Total de Instancias disponiveis: {total_disponiveis}") #Imprime a quantidade de instancias disponíveis
print (resposta["ResponseMetadata"]["HTTPStatusCode"]) #imprima o valor da chave ResponseMetadata
print (instancias_oracle) #imprima a lista instancias_oracle