from dbre.calculos import calcular_percentual, classificar_status #Importa as funções de cálculo de percentual e classificação de status do módulo dbre.calculos.


def transformar_resultados(resultados): #Define a função transformar_resultados que recebe uma lista de resultados como argumento.
    relatorio = [] #Cria uma lista vazia chamada relatorio

    for ( # Desempacota cada tupla de resultados em variáveis individuais.
        nome, #Nome do tablespace
        total_bytes, #Total de bytes alocados
        usado_bytes, #Total de bytes usados
        max_bytes, #Total de bytes máximos permitidos
        total_arquivos, #Total de arquivos de dados
        arquivos_autoextend #Arquivos com autoextend habilitado
    ) in resultados: #Em seguida, itera sobre cada tupla de resultados.
        total_gb = total_bytes / 1024 ** 3 #Converte o total de bytes para gigabytes e atribui à variável total_gb.
        usado_gb = usado_bytes / 1024 ** 3 #Converte o total de bytes usados para gigabytes e atribui à variável usado_gb.
        max_gb = max_bytes / 1024 ** 3 #Converte o total de bytes máximos para gigabytes e atribui à variável max_gb.

        percentual = calcular_percentual( #Calcula o percentual de uso do tablespace chamando a função calcular_percentual com os argumentos total_bytes e usado_bytes.
            total_bytes, #argumento total_bytes
            usado_bytes #argumento usado_bytes
        )

        status = classificar_status(percentual) #Atribiui o status do tablespace chamando a função classificar_status com o argumento percentual.

        registro = { #Cria um dicionário chamado registro com as informações do tablespace, incluindo nome, total em GB, usado em GB, percentual de uso e status.
            "tablespace": nome,
            "total_gb": round(total_gb, 2),
            "usado_gb": round(usado_gb, 2),
            "percentual": round(percentual, 1),
            "status": status
        }

        relatorio.append(registro) #Adiciona o dicionário registro à lista relatorio.

    return relatorio #Retorna a lista relatorio contendo os registros transformados.