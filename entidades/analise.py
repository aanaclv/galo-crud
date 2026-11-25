import json

from entidades.regras_diagnostico import gerar_diagnostico, validar_dados, classificar_ph, classificar_fosforo, classificar_potassio

def listar_diagnosticos():

    try:
        with open("database/db_analise.json", "r", encoding="utf-8") as arquivo:
            banco = json.load(arquivo)

        return banco["diagnosticos"]

    except FileNotFoundError:
        print("Arquivo de diagnósticos não encontrado.")
        return []

    except json.JSONDecodeError:
        print("Erro: o arquivo JSON está inválido.")
        return []


def exibir_diagnosticos():

    diagnosticos = listar_diagnosticos()

    for indice, diagnostico in enumerate(diagnosticos):
        print(f"\nDiagnóstico {indice + 1}:")
        print(diagnostico)

def cadastrar_diagnostico(diagnostico):

    banco = {"diagnosticos": listar_diagnosticos()}

    banco["diagnosticos"].append(diagnostico)

    try:
        with open("database/db_analise.json", "w", encoding="utf-8") as arquivo:
            json.dump(banco, arquivo, indent=4, ensure_ascii=False)

        return "Diagnóstico cadastrado com sucesso."

    except Exception as erro:
        return f"Erro ao cadastrar diagnóstico: {erro}"

def atualizar_diagnostico(indice, novo_diagnostico):

    banco = {"diagnosticos": listar_diagnosticos()}

    if indice < 0 or indice >= len(banco["diagnosticos"]):
        return "Diagnóstico não encontrado."

    banco["diagnosticos"][indice] = novo_diagnostico

    try:
        with open("database/db_analise.json", "w", encoding="utf-8") as arquivo:
            json.dump(banco, arquivo, indent=4, ensure_ascii=False)

        return "Diagnóstico atualizado com sucesso."

    except Exception as erro:
        return f"Erro ao atualizar diagnóstico: {erro}"

def excluir_diagnostico(indice):

    banco = {"diagnosticos": listar_diagnosticos()}

    if indice < 0 or indice >= len(banco["diagnosticos"]):
        return "Diagnóstico não encontrado."

    banco["diagnosticos"].pop(indice)

    try:
        with open("database/db_analise.json", "w", encoding="utf-8") as arquivo:
            json.dump(banco, arquivo, indent=4, ensure_ascii=False)

        return "Diagnóstico excluído com sucesso."

    except Exception as erro:
        return f"Erro ao excluir diagnóstico: {erro}"

def consultar_diagnostico(indice):

    diagnosticos = listar_diagnosticos()

    if indice < 0 or indice >= len(diagnosticos):
        return "Diagnóstico não encontrado."

    return diagnosticos[indice]