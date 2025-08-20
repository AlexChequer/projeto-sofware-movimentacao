from app_service import validar_campos

def test_validar_campos_completos():
    data = {
        "cpf_comprador": "123",
        "cpf_vendedor": "456",
        "ticker": "PETR4",
        "quantidade": 10
    }
    assert validar_campos(data) is None




