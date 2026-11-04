from services.solo import *
from services.usuario import *

propriedade = input("Insira o nome da sua propriedade: ")
localizacao = input("Insira a cidade: ")
area = int(input("Insira o tamanho da sua propridade em m2: "))
plantacao = input("Insira o tipo de plantação: ")

print(cadastrar_solo(propriedade, localizacao, area, plantacao))
listar_solo()


nome = input("Insira seu nome: ")
email = input("Insira seu email: ")
senha = input("Insira sua senha: ")
print(cadastrar_usuario(nome, email, senha))
listar_usuario()
atualizar_usuario()