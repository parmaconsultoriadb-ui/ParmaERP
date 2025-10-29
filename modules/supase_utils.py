"""Helpers reutilizáveis para comunicação com o Supabase."""

from __future__ import annotations

import os
from typing import Any, Dict, Iterable, Optional

import streamlit as st
from supabase import Client, create_client


class SupabaseCredentialsError(RuntimeError):
    """Erro específico para indicar problemas com as credenciais do Supabase."""


def _get_secret(name: str) -> Optional[str]:
    """Obtém um segredo do Streamlit ou variável de ambiente de forma segura."""

    # A API de st.secrets não possui o método .get(), por isso tratamos manualmente
    try:
        if name in st.secrets:  # type: ignore[operator]
            return st.secrets[name]
    except Exception:
        # Quando st.secrets não está configurado (ex.: execução local sem secrets.toml)
        pass

    return os.getenv(name)


def _load_credentials() -> tuple[str, str]:
    """Carrega as credenciais necessárias para inicializar o cliente Supabase."""

    url = _get_secret("SUPABASE_URL")
    key = _get_secret("SUPABASE_ANON_KEY")

    if not url or not key:
        raise SupabaseCredentialsError(
            "Credenciais do Supabase não configuradas. Informe SUPABASE_URL e SUPABASE_ANON_KEY "
            "em st.secrets ou em variáveis de ambiente."
        )

    return url, key


@st.cache_resource(show_spinner=False)
def get_client() -> Client:
    """Retorna um cliente Supabase reutilizável."""

    url, key = _load_credentials()
    return create_client(url, key)


def _execute_table_operation(
    table: str, operation: str, *, payload: Optional[Dict[str, Any]] = None, match: Optional[Dict[str, Any]] = None
) -> Iterable[Dict[str, Any]]:
    """Executa uma operação na tabela e padroniza o tratamento de erros."""

    client = get_client()

    try:
        query = client.table(table)

        if operation == "select":
            response = query.select("*").execute()
        elif operation == "insert":
            if payload is None:
                raise ValueError("Payload obrigatório para inserção no Supabase.")
            response = query.insert(payload).execute()
        elif operation == "update":
            if payload is None or match is None:
                raise ValueError("Payload e critério são obrigatórios para atualização no Supabase.")
            response = query.update(payload).match(match).execute()
        elif operation == "delete":
            if match is None:
                raise ValueError("Critério obrigatório para exclusão no Supabase.")
            response = query.delete().match(match).execute()
        else:
            raise ValueError(f"Operação não suportada: {operation}")
    except Exception as exc:  # pragma: no cover - streamlit apps não possuem testes automatizados
        raise RuntimeError(f"Erro ao executar operação '{operation}' na tabela '{table}': {exc}") from exc

    return response.data or []


def sb_listar_registros(tabela: str) -> Iterable[Dict[str, Any]]:
    """Lista todos os registros de uma tabela no Supabase."""

    return _execute_table_operation(tabela, "select")


def sb_insert(tabela: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Insere um novo registro e retorna o resultado."""

    data = list(_execute_table_operation(tabela, "insert", payload=payload))
    return data[0] if data else {}


def sb_update_by_id(tabela: str, id_registro: Any, payload: Dict[str, Any]) -> None:
    """Atualiza um registro com base no ID fornecido."""

    if id_registro is None:
        raise ValueError("O ID do registro não pode ser vazio para atualização.")

    _execute_table_operation(tabela, "update", payload=payload, match={"id": id_registro})


def sb_delete_by_id(tabela: str, id_registro: Any) -> None:
    """Remove um registro com base no ID fornecido."""

    if id_registro is None:
        raise ValueError("O ID do registro não pode ser vazio para exclusão.")

    _execute_table_operation(tabela, "delete", match={"id": id_registro})
