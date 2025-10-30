from adapters.supabase_repo import list_rows, insert_row, update_row
from common.config import agora_datetime, settings

TABLE = "comercial"

def listar(page: int = 1, busca: str = None):
    if busca:
        return list_rows(TABLE, page=page, ilike=("cliente", busca), order_by="id", desc=True)
    return list_rows(TABLE, page=page, order_by="id", desc=True)

def criar(data: dict):
    data["data"] = agora_datetime().strftime(settings.DATE_FORMAT)
    data["atualizacao"] = agora_datetime().strftime(settings.DATETIME_FORMAT)
    return insert_row(TABLE, data)

def mover_status(row_id: int, novo_status: str):
    campos = {"status": novo_status, "atualizacao": agora_datetime().strftime(settings.DATETIME_FORMAT)}
    return update_row(TABLE, row_id, campos, id_col="id")
