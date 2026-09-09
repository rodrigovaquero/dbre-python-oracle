from dbre.relatorio import transformar_resultados

def test_transformar_resultados():
    resultados = [
        (
            "SYSTEM",
            10 * 1024 ** 3,
            9 * 1024 ** 3,
            20 * 1024 ** 3,
            1,
            1
        )
    ]

    relatorio = transformar_resultados(resultados)