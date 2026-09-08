import pytest
from dbre.calculos import calcular_percentual, classificar_status

def test_calcular_percentual():
    resultado = calcular_percentual(500, 300)

    assert resultado == 60.0

def test_classificar_status_critica():
    status = classificar_status(95)

    assert status == "CRÍTICA"    

def test_classificar_status_alerta():
    status = classificar_status(94.9)

    assert status == "ALERTA"    

def test_classificar_status_normal():
    status = classificar_status(89.9)

    assert status == "NORMAL"    

def test_calcular_percentual_total_zero():
    with pytest.raises(ZeroDivisionError):
        calcular_percentual(0, 0)  