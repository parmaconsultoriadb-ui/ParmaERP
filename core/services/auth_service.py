USUARIOS = {
    "admin":   {"senha": "Parma!123@", "permissoes": ["menu", "clientes", "vagas", "candidatos", "logs", "comercial", "contratos"]},
    "andre":   {"senha": "And!123@",   "permissoes": ["clientes", "vagas", "candidatos", "comercial"]},
    "lorrayne":{"senha": "Lrn!123@",   "permissoes": ["vagas", "candidatos"]},
    "nikole":  {"senha": "Nkl!123@",   "permissoes": ["vagas", "candidatos"]},
    "julia":   {"senha": "Jla!123@",   "permissoes": ["vagas", "candidatos"]},
    "ricardo": {"senha": "Rcd!123@",   "permissoes": ["clientes", "vagas", "comercial"]},
    "leila":   {"senha": "Lel!123@",   "permissoes": ["vagas", "candidatos"]},
    "kaline":  {"senha": "Kln!123@",   "permissoes": ["vagas", "candidatos"]}
}

def login(usuario: str, senha: str):
    if usuario in USUARIOS and senha == USUARIOS[usuario]["senha"]:
        return True, USUARIOS[usuario]["permissoes"]
    return False, []

def get_permissoes(usuario: str):
    return USUARIOS.get(usuario, {}).get("permissoes", [])
