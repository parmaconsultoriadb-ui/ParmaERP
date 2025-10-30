import uuid
from typing import List, Dict, Any, Optional
from adapters.supabase_repo import ClientesRepo
from schemas.clientes import Cliente
from common.errors import NotFoundError

class ClientesService:
    def __init__(self):
        self.repo = ClientesRepo()

    def listar_clientes(self, page: int = 1, busca: Optional[str] = None) -> List[Dict[str, Any]]:
        return self.repo.list(page=page, search_col="nome", search=busca)

    def criar_cliente(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Gera ID se não vier
        payload = {"id": data.get("id") or f"c_{uuid.uuid4().hex[:8]}", **data}
        cliente = Cliente(**payload)  # validação
        return self.repo.insert(cliente.model_dump())

    def obter_cliente(self, cliente_id: str) -> Dict[str, Any]:
        obj = self.repo.get_by_id(cliente_id)
        if not obj:
            raise NotFoundError("Cliente não encontrado")
        return obj
