from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.app import app, gastos, buscar_cotacao_dolar
import pytest


@pytest.fixture(autouse=True)
def limpar_gastos():
    gastos.clear()
    yield
    gastos.clear()


client = TestClient(app)


# -------------------------------------------------------
# Teste 1: verifica que buscar_cotacao_dolar() retorna
# um float correto quando a API responde normalmente.
# -------------------------------------------------------
def test_buscar_cotacao_dolar_sucesso():
    resposta_falsa = MagicMock()
    resposta_falsa.json.return_value = {"USDBRL": {"bid": "5.25"}}
    resposta_falsa.raise_for_status.return_value = None

    with patch("src.app.requests.get", return_value=resposta_falsa):
        cotacao = buscar_cotacao_dolar()

    assert isinstance(cotacao, float)
    assert cotacao == 5.25


# -------------------------------------------------------
# Teste 2: verifica que GET /total/dolar faz o cálculo
# correto de conversão via endpoint HTTP.
# -------------------------------------------------------
def test_endpoint_total_em_dolar():
    client.post("/gastos", json={"valor": 105.0, "descricao": "supermercado"})

    resposta_falsa = MagicMock()
    resposta_falsa.json.return_value = {"USDBRL": {"bid": "5.25"}}
    resposta_falsa.raise_for_status.return_value = None

    with patch("src.app.requests.get", return_value=resposta_falsa):
        resposta = client.get("/total/dolar")

    assert resposta.status_code == 200
    dados = resposta.json()
    assert dados["total_brl"] == 105.0
    assert dados["cotacao_usd_brl"] == 5.25
    assert dados["total_usd"] == 20.0  # 105 / 5.25 = 20.0


# -------------------------------------------------------
# Teste 3: verifica que o endpoint retorna 503 quando
# a API externa está fora do ar.
# -------------------------------------------------------
def test_endpoint_total_dolar_api_indisponivel():
    client.post("/gastos", json={"valor": 50.0, "descricao": "teste"})

    with patch("src.app.requests.get", side_effect=Exception("Connection refused")):
        resposta = client.get("/total/dolar")

    assert resposta.status_code == 503
    assert "Erro ao buscar cotação" in resposta.json()["detail"]