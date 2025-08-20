from app import app, movimentacoes
import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_movimentacoes(client):
    movimentacoes.clear()
    movimentacoes.append({
        "cpf_comprador": '111',
        "cpf_vendedor": "222",
        "ticker": "VALE3",
        "quantidade": 2,
        "valor_movimentacao": 124.6
    })

    response = client.get("/movimentacoes")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['ticker'] == "VALE3"


@patch("app.criar_objeto_movimentacao")
@patch("app.calcular_valor", return_value=(1000, None))
def test_post_movimentacoes(mock_calcular, mock_criar, client):
    movimentacoes.clear()
    payload = {
        "cpf_comprador": "123",
        "cpf_vendedor": "456",
        "ticker": "PETR4",
        'quantidade': 10
    }

    mock_criar.side_effect = lambda data, valor: {
        "cpf_comprador": data['cpf_comprador'],
        "cpf_vendedor": data['cpf_vendedor'],
        'ticker': data['ticker'],
        'quantidade': data['quantidade'],
        'valor': valor
    }


    response = client.post("/movimentacoes", json=payload)

    assert response.status_code == 201
    data = response.get_json()
    assert data['valor'] == 1000
    assert data['cpf_comprador'] == '123'
    assert data['cpf_vendedor'] == '456'
    assert data['ticker'] == "PETR4"

