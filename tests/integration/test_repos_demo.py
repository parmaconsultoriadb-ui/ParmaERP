from adapters.supabase_repo import ClientesRepo

def test_clientes_repo_demo_list_insert():
    repo = ClientesRepo()
    base = repo.list(page=1)
    n = len(base)
    repo.insert({"id": "c_test", "nome": "Teste", "email": None, "cnpj": None})
    novo = repo.list(page=1)
    assert len(novo) == n + 1
