import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from database.db import consultar_db, salvar_db

def cadastrar_solo(propriedade, localizacao, area, plantacao):

    banco = consultar_db("db_solo")

    if banco is None:
        return "Erro ao acessar banco."

    novo_id = len(banco["solo"]) + 1

    solo = {
        "id": novo_id,
        "propriedade": propriedade,
        "localizacao": localizacao,
        "area": area,
        "plantacao": plantacao
    }

    banco["solo"].append(solo)

    #tratamento
    if salvar_db("db_solo", banco):
        return f"solo da propriedade {propriedade} cadastrado."
    return "erro ao salvar solo."

def listar_solo():

    banco = consultar_db("db_solo")

    # tratamento
    if banco is None:
        print("Erro ao acessar o banco.")
        return

    if len(banco["solo"]) == 0:
        print("Nenhum solo cadastrado.")
        return

    print("\n==== listagem dos solos ====")

    for indice, solo in enumerate(banco["solo"]):
        print(f"id: {solo.get('id','N/A')}")
        print(f"Propriedade: {solo.get('propriedade', 'N/A')}")
        print(f"Localização: {solo.get('localizacao', solo.get('cidade', 'N/A'))}")
        print(f"Área: {solo.get('area', 'N/A')} ha")
        print(f"Plantação: {solo.get('plantacao', 'N/A')}")
        print("-" * 40)