from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(title="Gerenciador de Gastos", version="2.0.0")

# Banco de dados em memória (igual ao projeto original)
gastos: list[dict] = []


# -------------------------------------------------
# Schema de entrada (Pydantic valida automaticamente)
# -------------------------------------------------
class Gasto(BaseModel):
    valor: float
    descricao: str


# -------------------------------------------------
# Rotas CRUD
# -------------------------------------------------

@app.get("/")
def raiz():
    return {"mensagem": "Gerenciador de Gastos — API online ✅"}


@app.post("/gastos", status_code=201)
def adicionar_gasto(gasto: Gasto):
    if gasto.valor < 0:
        raise HTTPException(status_code=400, detail="Valor não pode ser negativo")
    gastos.append({"valor": gasto.valor, "descricao": gasto.descricao})
    return {"mensagem": "Gasto adicionado", "gasto": gasto}


@app.get("/gastos")
def listar_gastos():
    return {"gastos": gastos}


@app.get("/total")
def ver_total():
    return {"total_brl": sum(g["valor"] for g in gastos)}


@app.delete("/gastos/{index}", status_code=200)
def remover_gasto(index: int):
    if index < 0 or index >= len(gastos):
        raise HTTPException(status_code=404, detail="Índice inválido")
    removido = gastos.pop(index)
    return {"mensagem": "Gasto removido", "gasto": removido}


# -------------------------------------------------
# Integração com API de câmbio (AwesomeAPI)
# -------------------------------------------------

def buscar_cotacao_dolar() -> float:
    """Busca a cotação atual do dólar em reais via AwesomeAPI."""
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    resposta = requests.get(url, timeout=5)
    resposta.raise_for_status()
    dados = resposta.json()
    return float(dados["USDBRL"]["bid"])


@app.get("/total/dolar")
def ver_total_em_dolar():
    """Retorna o total dos gastos convertido para dólares (USD)."""
    try:
        cotacao = buscar_cotacao_dolar()
        total_brl = sum(g["valor"] for g in gastos)
        total_usd = round(total_brl / cotacao, 2)
        return {
            "total_brl": total_brl,
            "cotacao_usd_brl": cotacao,
            "total_usd": total_usd,
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Erro ao buscar cotação: {str(e)}")