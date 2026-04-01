from src.app import adicionar, total, remover, gastos
import pytest


def setup_function():
    gastos.clear()


def test_adicionar_gasto():
    adicionar(50, "mercado")
    assert total() == 50


def test_valor_negativo():
    with pytest.raises(ValueError):
        adicionar(-10, "erro")


def test_remover_gasto():
    adicionar(20, "lanche")
    remover(0)
    assert total() == 0