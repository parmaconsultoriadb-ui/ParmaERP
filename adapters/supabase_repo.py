from typing import Any, Dict, List, Optional, Tuple
from adapters.supabase_client import get_supabase
from common.config import settings

PAGE_SIZE = settings.PAGE_SIZE

def _range_for_page(page: int, page_size: int = PAGE_SIZE) -> Tuple[int, int]:
    start = (page - 1) * page_size
    end = start + page_size - 1
    return start, end

# ---------- GENÉRICOS ----------
def list_rows(
    table: str,
    page: int = 1,
    page_size: int = PAGE_SIZE,
    where: Optional[Dict[str, Any]] = None,
    ilike: Optional[Tuple[str, str]] = None,
    order_by: str = "created_at",
    desc: bool = True,
) -> List[Dict[str, Any]]:
    sb = get_supabase()
    q = sb.table(table).select("*")
    if where:
        for k, v in where.items():
            q = q.eq(k, v)
    if ilike:
        col, txt = ilike
        q = q.ilike(col, f"%{txt}%")
    q = q.order(order_by, desc=desc)
    start, end = _range_for_page(page, page_size)
    return q.range(start, end).execute().data

def get_row(table: str, row_id: Any, id_col: str = "id") -> Optional[Dict[str, Any]]:
    sb = get_supabase()
    res = sb.table(table).select("*").eq(id_col, row_id).single().execute()
    return res.data if res.data else None

def insert_row(table: str, data: dict) -> dict:
    sb = get_supabase()
    res = sb.table(table).insert(data).select("*").execute()
    # retorno compatível com a estrutura moderna
    return res.data[0] if res.data else {}

def update_row(table: str, row_id: any, data: dict, id_col: str = "id") -> dict:
    sb = get_supabase()
    res = sb.table(table).update(data).eq(id_col, row_id).select("*").execute()
    return res.data[0] if res.data else {}

def delete_row(table: str, row_id: Any, id_col: str = "id") -> None:
    sb = get_supabase()
    sb.table(table).delete().eq(id_col, row_id).execute()
