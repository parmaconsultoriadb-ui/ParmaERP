from schemas.clientes import Cliente
from schemas.comercial import Oportunidade
from schemas.recrutamento import Candidato, Vaga

def test_cliente_schema():
    c = Cliente(id="c123", nome="Empresa X", email="contato@x.com", cnpj="12345678000100")
    assert c.nome == "Empresa X"

def test_oportunidade_schema():
    o = Oportunidade(id="o1", cliente_id="c123", valor=1000.0, fase="Proposta")
    assert o.valor == 1000.0

def test_recrutamento_schemas():
    k = Candidato(id="k1", nome="Maria")
    v = Vaga(id="v1", titulo="Dev")
    assert k.status == "Novo"
    assert v.status == "Aberta"
