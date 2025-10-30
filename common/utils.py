import pandas as pd
import streamlit as st

def next_id(df: pd.DataFrame, id_col="id") -> int:
    if df is None or df.empty or id_col not in df.columns:
        return 1
    vals = pd.to_numeric(df[id_col], errors="coerce").fillna(0).astype(int)
    return int(vals.max()) + 1

def download_button(df: pd.DataFrame, filename: str, label="⬇️ Baixar CSV"):
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(label=label, data=csv, file_name=filename, mime="text/csv", use_container_width=True)
