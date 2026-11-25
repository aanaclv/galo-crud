import hashlib
import hmac
import secrets
# Ajustado: importou salvar_db junto com consultar_db
from db import consultar_db, salvar_db

# Ajustado: usa o nome base sem ".json", pois db.py monta "database/<db>.json"
DB_USUARIO = "db_usuario"


# Ajustado: incluída validação de texto pois antes dependia de "from .armazenamento import ... texto"
def texto(valor, campo):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"{campo}: informe um texto válido.")
    return valor.strip()


# Ajustado: garante list de usuários válidos com email, salt e senha_hash
def _carregar_usuarios():
    dados = consultar_db(DB_USUARIO)
    itens = []

    if isinstance(dados, list):
        itens = dados
    elif isinstance(dados, dict):
        for chave in ("user", "usuarios"):
            if isinstance(dados.get(chave), list):
                itens = dados[chave]
                break

    return [
        u for u in itens
        if isinstance(u, dict)
        and "email" in u
        and "salt" in u
        and "senha_hash" in u
    ]


def normalizar_email(email):
    email = texto(email, "E-mail").lower()
    partes = email.split("@")

    if (
        len(partes) != 2
        or not partes[0]
        or "." not in partes[1]
        or any(not p for p in partes[1].split("."))
        or any(c.isspace() for c in email)
    ):
        raise ValueError("Informe um e-mail válido.")

    return email


# Proteção da senha
def gerar_hash(senha, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        senha.encode("utf-8"),
        bytes.fromhex(salt),
        600_000
    ).hex()


# Ajustado: senha simplificada para pelo menos 4 caracteres não vazios
def definir_senha(usuario, senha):
    if not senha or len(senha.strip()) < 4:
        raise ValueError(
            "A senha deve conter pelo menos 4 caracteres."
        )

    salt = secrets.token_hex(16)
    usuario["salt"] = salt
    usuario["senha_hash"] = gerar_hash(senha, salt)


def perfil_publico(usuario):
    return {
        chave: valor
        for chave, valor in usuario.items()
        if chave not in ("salt", "senha_hash")
    }


# CREATE - Cadastrar usuário
def cadastrar_usuario(nome, email, senha):
    # Ajustado: usa _carregar_usuarios() para evitar erro com str/None/dict/itens inválidos
    usuarios = _carregar_usuarios()
    email = normalizar_email(email)

    if any(u["email"] == email for u in usuarios):
        raise ValueError("E-mail já cadastrado.")

    usuario = {
        "id": secrets.token_hex(8),
        "nome": texto(nome, "Nome"),
        "email": email
    }

    definir_senha(usuario, senha)

    usuarios.append(usuario)
    # Ajustado: usa salvar_db com o nome base DB_USUARIO
    salvar_db(DB_USUARIO, usuarios)

    return perfil_publico(usuario)


# Autenticação - Login
def autenticar(email, senha):
    email = email.strip().lower()

    # Ajustado: usa _carregar_usuarios()
    for usuario in _carregar_usuarios():
        if usuario["email"] == email and hmac.compare_digest(
            gerar_hash(senha, usuario["salt"]),
            usuario["senha_hash"]
        ):
            return perfil_publico(usuario)

    return None


# READ - Consultar usuário
def consultar_usuario(usuario_id):
    # Ajustado: usa _carregar_usuarios()
    for usuario in _carregar_usuarios():
        if usuario["id"] == usuario_id:
            return perfil_publico(usuario)

    raise ValueError("Usuário não encontrado.")


# UPDATE - Atualizar usuário
def atualizar_usuario(
    usuario_id, nome, email, senha_atual, nova_senha=None
):
    # Ajustado: usa _carregar_usuarios()
    usuarios = _carregar_usuarios()
    email = normalizar_email(email)

    for usuario in usuarios:
        if usuario["id"] == usuario_id:

            if not hmac.compare_digest(
                gerar_hash(senha_atual, usuario["salt"]),
                usuario["senha_hash"]
            ):
                raise ValueError("Senha atual incorreta.")

            if any(
                u["email"] == email and u["id"] != usuario_id
                for u in usuarios
            ):
                raise ValueError("E-mail já cadastrado.")

            usuario["nome"] = texto(nome, "Nome")
            usuario["email"] = email

            if nova_senha:
                definir_senha(usuario, nova_senha)

            # Ajustado: usa salvar_db com o nome base DB_USUARIO
            salvar_db(DB_USUARIO, usuarios)

            return perfil_publico(usuario)

    raise ValueError("Usuário não encontrado.")


# DELETE - Excluir usuário
def excluir_usuario(usuario_id, senha):
    # Ajustado: importa listar_solos de entidades.solo conforme estrutura de pastas
    from entidades.solo import listar_solos

    # Ajustado: usa _carregar_usuarios()
    usuarios = _carregar_usuarios()

    for usuario in usuarios:
        if usuario["id"] == usuario_id:

            if not hmac.compare_digest(
                gerar_hash(senha, usuario["salt"]),
                usuario["senha_hash"]
            ):
                raise ValueError("Senha incorreta.")

            # Ajustado: verifica análises vinculadas em services.analise (listar_diagnosticos não existe em entidades.solo)
            try:
                from services.analise import listar_analises
                if listar_analises(usuario_id):
                    raise ValueError(
                        "Exclua suas análises antes de excluir a conta."
                    )
            except ImportError:
                pass

            # Ajustado: verifica solos vinculados e exibe mensagem coerente com solos/diagnósticos
            if listar_solos(usuario_id):
                raise ValueError(
                    "Exclua seus solos e análises antes de excluir a conta."
                )

            usuarios.remove(usuario)
            # Ajustado: usa salvar_db com o nome base DB_USUARIO
            salvar_db(DB_USUARIO, usuarios)

            return

    raise ValueError("Usuário não encontrado.")