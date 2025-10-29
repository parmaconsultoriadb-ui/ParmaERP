def tela_clientes():
    st.title("👥 Clientes")
    st.caption("Cadastro e gerenciamento de clientes Parma Consultoria")

    # --- carregar registros
    clientes = list(sb_listar_registros("clientes"))
    df = pd.DataFrame(clientes)

    # --- botão para atualizar
    if st.button("🔄 Atualizar lista"):
        st.rerun()

    if not df.empty:
        st.dataframe(df[["id", "data", "cliente", "nome", "cidade", "uf", "telefone", "email"]],
                     use_container_width=True)
    else:
        st.info("Nenhum cliente cadastrado ainda.")

    st.divider()
    st.subheader("➕ Novo cliente")

    # --- formulário
    with st.form("novo_cliente"):
        col1, col2 = st.columns(2)
        with col1:
            data = st.date_input("Data", dt.date.today())
            cliente = st.text_input("Cliente *")
            nome = st.text_input("Nome")
            cidade = st.text_input("Cidade")
        with col2:
            uf = st.text_input("UF", max_chars=2)
            telefone = st.text_input("Telefone")
            email = st.text_input("E-mail")

        enviar = st.form_submit_button("Salvar cliente")

        if enviar:
            if not cliente.strip():
                st.warning("⚠️ Campo 'Cliente' é obrigatório.")
            else:
                novo = {
                    "data": str(data),
                    "cliente": cliente.strip(),
                    "nome": nome.strip(),
                    "cidade": cidade.strip(),
                    "uf": uf.strip().upper(),
                    "telefone": telefone.strip(),
                    "email": email.strip(),
                }
                res = sb_insert("clientes", novo)
                st.success(f"✅ Cliente '{cliente}' adicionado com sucesso (ID: {res.get('id')}).")
                st.rerun()

    st.divider()
    st.subheader("✏️ Editar / Excluir Cliente")

    if not df.empty:
        cliente_sel = st.selectbox(
            "Selecione o cliente",
            df["cliente"].tolist(),
            index=None,
            placeholder="Escolha um cliente para editar"
        )
        if cliente_sel:
            cliente_row = df[df["cliente"] == cliente_sel].iloc[0]
            col1, col2 = st.columns(2)
            with col1:
                novo_nome = st.text_input("Nome", cliente_row["nome"])
                nova_cidade = st.text_input("Cidade", cliente_row["cidade"])
                novo_uf = st.text_input("UF", cliente_row["uf"], max_chars=2)
                novo_telefone = st.text_input("Telefone", cliente_row["telefone"])
            with col2:
                novo_email = st.text_input("E-mail", cliente_row["email"])
                nova_data = st.date_input(
                    "Data",
                    value=pd.to_datetime(cliente_row["data"]).date() if cliente_row["data"] else dt.date.today()
                )

            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("💾 Atualizar cliente", use_container_width=True):
                    sb_update_by_id(
                        "clientes",
                        cliente_row["id"],
                        {
                            "data": str(nova_data),
                            "nome": novo_nome,
                            "cidade": nova_cidade,
                            "uf": novo_uf.upper(),
                            "telefone": novo_telefone,
                            "email": novo_email,
                        },
                    )
                    st.success("✅ Cliente atualizado com sucesso!")
                    st.rerun()
            with col_b:
                if st.button("🗑️ Excluir cliente", use_container_width=True):
                    sb_delete_by_id("clientes", cliente_row["id"])
                    st.warning("🗑️ Cliente removido.")
                    st.rerun()
