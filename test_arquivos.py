from dbre.arquivos import gerar_csv, gerar_json

def test_gerar_json(tmp_path):
    relatorio = [
        {
            "tablespace": "SYSTEM",
            "total_gb": 10.0,
            "usado_gb": 9.0,
            "percentual": 90.0,
            "status": "ALERTA"
        }
    ]

    caminho = tmp_path / "relatorio.json"

    caminho_gerado = gerar_json(relatorio, caminho)

    assert caminho_gerado.exists()  

def test_gerar_csv(tmp_path):
    relatorio = [
        {
            "tablespace": "SYSTEM",
            "total_gb": 10.0,
            "usado_gb": 9.0,
            "percentual": 90.0,
            "status": "ALERTA"
        }
    ]

    caminho = tmp_path / "relatorio.csv"

    caminho_gerado = gerar_csv(relatorio, caminho)

    assert caminho_gerado.exists()    