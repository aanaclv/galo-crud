import hashlib
import hmac
import secrets
from .armazenamento import carregar, salvar, texto

ARQUIVO = "db_usuario.json"


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


def definir_senha(usuario, senha):
    if len(senha) < 8 or not senha.strip():
        raise ValueError(
            "A senha deve conter pelo menos 8 caracteres."
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
    usuarios = carregar(ARQUIVO)
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
    salvar(ARQUIVO, usuarios)

    return perfil_publico(usuario)


# Autenticação - Login
def autenticar(email, senha):
    email = email.strip().lower()

    for usuario in carregar(ARQUIVO):
        if usuario["email"] == email and hmac.compare_digest(
            gerar_hash(senha, usuario["salt"]),
            usuario["senha_hash"]
        ):
            return perfil_publico(usuario)

    return None


# READ - Consultar usuário
def consultar_usuario(usuario_id):
    for usuario in carregar(ARQUIVO):
        if usuario["id"] == usuario_id:
            return perfil_publico(usuario)

    raise ValueError("Usuário não encontrado.")


# UPDATE - Atualizar usuário
def atualizar_usuario(
    usuario_id, nome, email, senha_atual, nova_senha=None
):
    usuarios = carregar(ARQUIVO)
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

            salvar(ARQUIVO, usuarios)

            return perfil_publico(usuario)

    raise ValueError("Usuário não encontrado.")


# DELETE - Excluir usuário
def excluir_usuario(usuario_id, senha):
    from .analise import listar_diagnosticos

    usuarios = carregar(ARQUIVO)

    for usuario in usuarios:
        if usuario["id"] == usuario_id:

            if not hmac.compare_digest(
                gerar_hash(senha, usuario["salt"]),
                usuario["senha_hash"]
            ):
                raise ValueError("Senha incorreta.")

            if listar_diagnosticos(usuario_id):
                raise ValueError(
                    "Exclua seus diagnósticos antes de excluir a conta."
                )

            usuarios.remove(usuario)
            salvar(ARQUIVO, usuarios)

            return

    raise ValueError("Usuário não encontrado.")