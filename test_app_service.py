from app_service import validar_campos, calcular_valor
from unittest.mock import patch, MagicMock
import requests

def test_validar_campos_completos():
    data = {
        "cpf_comprador": "123",
        "cpf_vendedor": "456",
        "ticker": "PETR4",
        "quantidade": 10
    }
    assert validar_campos(data) is None

def test_validar_campos_incompletos():
    data = {
        "cpf_comprador": "123",
        "cpf_vendedor": "456",
        "ticker": "PETR4"
    }
    assert validar_campos(data) == "Campo obrigatório 'quantidade' não informado"

# Testes calcular valor

@patch("app_service.requests.get")
def test_calcular_valor_ok(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'ticker': "PETR", 'lastValue': 50}
    
    mock_get.return_value = mock_response

    valor, erro = calcular_valor('PETR', 10)

    assert valor == 500
    assert erro is None


@patch("app_service.requests.get")
def test_calcular_valor_badrequest(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.json.return_value = {'ticker': "PETR", 'last_value': 50}

    mock_get.return_value = mock_response

    valor, erro = calcular_valor("PETR", 10)

    assert valor is None
    assert erro == f"Erro ao buscar ticker 'PETR'"


@patch("app_service.requests.get", )
def test_calcular_valor_exception(mock_get):
    mock_response = MagicMock()
    mock_response.side_effect = requests.RequestException
    
    mock_get.side_effect = mock_response

    valor, erro = calcular_valor('PETR', 10)

    assert valor is None
    assert "Erro de conexão:" in erro

