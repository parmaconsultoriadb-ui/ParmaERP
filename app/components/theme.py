import streamlit as st

def apply_parma_theme():
    st.markdown(
        """
        <style>
        :root {
            --parma-blue-dark: #004488;
            --parma-blue-medium: #0066AA;
            --parma-blue-light: #E0F2F7;
            --parma-text-dark: #333333;
        }
        div.stButton > button {
            background-color: var(--parma-blue-dark) !important;
            color: white !important;
            border-radius: 8px;
            height: 2.5em;
            font-size: 14px;
            font-weight: bold;
            border: none;
        }
        div.stButton > button:hover { background-color: var(--parma-blue-medium) !important; }
        .topnav { background-color: #1E88E5; overflow: hidden; border-radius: 6px; }
        .topnav a {
            float: left; color: #f2f2f2; text-align: center; padding: 10px 16px;
            text-decoration: none; font-size: 16px; font-weight: 600;
        }
        .topnav a:hover { background-color: #1565C0; color: white; }
        .topnav a.active { background-color: #0D47A1; color: white; }
        hr.parma-hr { border: none; border-bottom: 1px solid #e0e0e0; margin: 0; }
        </style>
        """,
        unsafe_allow_html=True
    )
