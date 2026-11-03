#Como utilizar as funções para cadastrar solo e usuário no sistema:

from db import cadastrar_solo, cadastrar_usuario

nome = input("Insira seu nome: ")
email = input("Insira seu email: ")
senha = input("Insira sua senha: ")

print(cadastrar_usuario(nome, email, senha, id))


propriedade = input("Insira o nome da sua propriedade: ")
cidade = input("Insira a cidade: ")
area = int(input("Insira o tamanho da sua propridade em m2: "))
plantacao = input("Insira o tipo de plantação: ")

print(cadastrar_solo(propriedade, cidade, area, plantacao))