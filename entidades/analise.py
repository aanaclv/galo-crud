import json

FAIXA_PH_ADEQUADO = (5.5, 7.0)
FAIXA_FOSFORO_MEDIO = (10, 20)
FAIXA_POTASSIO_MEDIO = (50, 100)

def classificar_ph(ph):

    if ph < FAIXA_PH_ADEQUADO[0]:
        return "Ácido"

    elif FAIXA_PH_ADEQUADO[0] <= ph <= FAIXA_PH_ADEQUADO[1]:
        return "Adequado"

    else:
        return "Alcalino"

def classificar_fosforo(fosforo):

    if fosforo < FAIXA_FOSFORO_MEDIO[0]:
        return "Alta"

    elif FAIXA_FOSFORO_MEDIO[0] <= fosforo <= FAIXA_FOSFORO_MEDIO[1]:
        return "Média"

    else:
        return "Baixa"

def classificar_potassio(potassio):

    if potassio < FAIXA_POTASSIO_MEDIO[0]:
        return "Alta"

    elif FAIXA_POTASSIO_MEDIO[0] <= potassio <= FAIXA_POTASSIO_MEDIO[1]:
        return "Média"

    else:
        return "Baixa"

def gerar_diagnostico(ph, fosforo, potassio):

    if not validar_dados(ph, fosforo, potassio):
        raise ValueError("Os dados informados são inválidos.")

    diagnostico = {
        "ph": ph,
        "classificacao_ph": classificar_ph(ph),
        "fosforo": fosforo,
        "prioridade_fosforo": classificar_fosforo(fosforo),
        "potassio": potassio,
        "prioridade_potassio": classificar_potassio(potassio)
    }

    recomendacoes = []

    if ph < 5.5:
        recomendacoes.append("Aplicar correção da acidez do solo.")

    if FAIXA_FOSFORO_MEDIO[0] <= fosforo <= FAIXA_FOSFORO_MEDIO[1]:
        recomendacoes.append("Melhorar adubação fosfatada.")

    if potassio > 100:
        recomendacoes.append("Continuar acompanhando os níveis de potássio.")

    diagnostico["recomendacoes"] = recomendacoes

    return diagnostico

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

def validar_dados(ph, fosforo, potassio):

    if not isinstance(ph, (int, float)):
        return False

    if not isinstance(fosforo, (int, float)):
        return False

    if not isinstance(potassio, (int, float)):
        return False

    if ph < 0 or fosforo < 0 or potassio < 0:
        return False

    return True