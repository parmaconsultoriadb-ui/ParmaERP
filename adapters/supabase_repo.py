from typing import Any, Dict, List, Optional
from adapters.supabase_client import get_supabase
from common.config import settings

# ---- Banco DEMO em memória (para rodar sem Supabase) ----
_FAKE_DB = {
    "clientes": [
        {"id": "c1", "nome": "Acme SA", "email": "contato@acme.com", "cnpj": "12345678000100"},
        {"id": "c2", "nome": "Globex Ltda", "email": "sales@globex.com", "cnpj": "00998877000111"},
    ],
    "candidatos": [
        {"id": "k1", "nome": "Maria Silva", "email": "maria@exemplo.com", "status": "Em análise"},
    ],
    "vagas": [
        {"id": "v1", "titulo": "Desenvolvedor Python", "status": "Aberta"},
    ],
    "oportunidades": [
        {"id": "o1", "cliente_id": "c1", "valor": 15000.0, "fase": "Proposta"},
    ],
}


class BaseRepo:
    table_name: str

    def __init__(self, table_name: str):
        self.table_name = table_name
        self.sb = get_supabase()

    def list(
        self,
        page: int = 1,
        page_size: int = settings.PAGE_SIZE,
        search_col: Optional[str] = None,
        search: Optional[str] = None,
        order_col: str = "created_at",
        desc: bool = True,
    ) -> List[Dict[str, Any]]:
        if self.sb is None:
            items = _FAKE_DB.get(self.table_name, [])
            if search and search_col:
                items = [r for r in items if search.lower() in str(r.get(search_col, "")).lower()]
            start = (page - 1) * page_size
            end = start + page_size
            return items[start:end]

        query = self.sb.table(self.table_name).select("*")
        if search and search_col:
            query = query.ilike(search_col, f"%{search}%")
        query = query.order(order_col, desc=desc)
        start = (page - 1) * page_size
        end = start + page_size - 1
        return query.range(start, end).execute().data

    def get_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        if self.sb is None:
            for r in _FAKE_DB.get(self.table_name, []):
                if r.get("id") == item_id:
                    return r
            return None

        res = self.sb.table(self.table_name).select("*").eq("id", item_id).single().execute()
        return res.data if res.data else None

    def insert(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if self.sb is None:
            _FAKE_DB[self.table_name].append(data)
            return data
        res = self.sb.table(self.table_name).insert(data).select("*").single().execute()
        return res.data

    def update(self, item_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if self.sb is None:
            for idx, r in enumerate(_FAKE_DB[self.table_name]):
                if r.get("id") == item_id:
                    _FAKE_DB[self.table_name][idx] = {**r, **data}
                    return _FAKE_DB[self.table_name][idx]
            raise KeyError("ID não encontrado no modo DEMO")
        res = self.sb.table(self.table_name).update(data).eq("id", item_id).select("*").single().execute()
        return res.data

    def delete(self, item_id: str) -> None:
        if self.sb is None:
            _FAKE_DB[self.table_name] = [r for r in _FAKE_DB[self.table_name] if r.get("id") != item_id]
            return
        self.sb.table(self.table_name).delete().eq("id", item_id).execute()


class ClientesRepo(BaseRepo):
    def __init__(self):
        super().__init__("clientes")


class CandidatosRepo(BaseRepo):
    def __init__(self):
        super().__init__("candidatos")


class VagasRepo(BaseRepo):
    def __init__(self):
        super().__init__("vagas")


class ComercialRepo(BaseRepo):
    def __init__(self):
        super().__init__("oportunidades")
