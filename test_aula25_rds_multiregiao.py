import pytest

from aula25_rds_multiregiao import (
    criar_resumo,
    eh_oracle,
    esta_disponivel,
    contar_instancias
)

from unittest.mock import Mock

@pytest.mark.parametrize(
    "engine, esperado",
    [
        ("oracle-se2", True),
        ("postgres", False)
    ]
)
def test_eh_oracle(engine, esperado):
    db_instance = {
        "Engine": engine
    }

    resultado = eh_oracle(db_instance)

    assert resultado is esperado

@pytest.mark.parametrize(
    "status, esperado",
    [
        ("available", True),
        ("stopped", False)
    ]
)
def test_esta_disponivel(status, esperado):
    db_instance = {
        "DBInstanceStatus": status
    }

    resultado = esta_disponivel(db_instance)

    assert resultado is esperado

def test_criar_resumo ():
    total_instancias = 3
    total_oracle = 2
    total_disponiveis = 2

    resultado = criar_resumo(total_instancias, total_oracle, total_disponiveis)

    assert resultado == {
        "total_rds": total_instancias,
        "total_oracle": total_oracle,
        "total_disponiveis": total_disponiveis
    }

def test_contar_instancias():
    paginador = Mock()

    paginador.paginate.return_value = [
        {
            "DBInstances": [
                {
                    "Engine": "oracle-se2",
                    "DBInstanceStatus": "available"
            }
            ]
        }
    ]

    resultado = contar_instancias(paginador)

    assert resultado == {
        "total_rds": 1,
        "total_oracle": 1,
        "total_disponiveis": 1
    }