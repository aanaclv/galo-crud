import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from database.db import consultar_db, salvar_db

def cadastrar_usuario(nome, email, senha):

    banco = consultar_db("db_usuario")

    if banco is None:
        return "Erro ao acessar o banco."

    novo_id = len(banco["user"]) + 1

    usuario = {
        "id": novo_id,
        "nome": nome,
        "email": email,
        "senha": senha
    }

    banco["user"].append(usuario)

    if salvar_db("db_usuario", banco):
        return f"usuário {nome} cadastrado com sucesso."

    return "erro ao salvar usuário."

def listar_usuario():

    banco = consultar_db("db_usuario")

    # tratamento
    if banco is None:
        print("Erro ao acessar o banco.")
        return

    if len(banco["user"]) == 0:
        print("Nenhum usuário cadastrado.")
        return

    print("\n==== listagem dos usuarios ====")

    for indice, usuario in enumerate(banco["user"]):
        print(f"id: {usuario.get('id','N/A')}")
        print(f"nome: {usuario.get('nome','N/A')}")
        print(f"email: {usuario.get('email','N/A')}")
        print("-" * 40)


def atualizar_usuario():

    banco = consultar_db("db_usuario")

    if banco is None:
        print("erro ao acessar banco.")
        return

    listar_usuario()

    id_procurado = int(input("digite o ID do usuário que deseja atualizar: "))

    for usuario in banco["user"]:
        if usuario["id"] == id_procurado:
            novo_nome = input("digite o novo nome: ")
            novo_email = input("digite o novo email: ")
            nova_senha = input("digite a nova senha: ")

            usuario["nome"] = novo_nome
            usuario["email"] = novo_email
            usuario["senha"] = nova_senha

            if salvar_db("db_usuario", banco):
                print("usuário atualizado")
            else:
                print("erro ao salvar a atualização")
            
            return
    print("usuário não encontrado")