from fastapi.testclient import TestClient
from src.app import app, gastos
import pytest


@pytest.fixture(autouse=True)
def limpar_gastos():
    """Limpa a lista de gastos antes de cada teste."""
    gastos.clear()
    yield
    gastos.clear()


client = TestClient(app)


def test_adicionar_gasto():
    resposta = client.post("/gastos", json={"valor": 50.0, "descricao": "mercado"})
    assert resposta.status_code == 201
    assert resposta.json()["gasto"]["valor"] == 50.0


def test_valor_negativo():
    resposta = client.post("/gastos", json={"valor": -10.0, "descricao": "erro"})
    assert resposta.status_code == 400


def test_listar_gastos():
    client.post("/gastos", json={"valor": 30.0, "descricao": "lanche"})
    resposta = client.get("/gastos")
    assert resposta.status_code == 200
    assert len(resposta.json()["gastos"]) == 1


def test_ver_total():
    client.post("/gastos", json={"valor": 100.0, "descricao": "supermercado"})
    client.post("/gastos", json={"valor": 50.0, "descricao": "farmácia"})
    resposta = client.get("/total")
    assert resposta.json()["total_brl"] == 150.0


def test_remover_gasto():
    client.post("/gastos", json={"valor": 20.0, "descricao": "lanche"})
    resposta = client.delete("/gastos/0")
    assert resposta.status_code == 200
    assert client.get("/total").json()["total_brl"] == 0.0


def test_remover_indice_invalido():
    resposta = client.delete("/gastos/999")
    assert resposta.status_code == 404