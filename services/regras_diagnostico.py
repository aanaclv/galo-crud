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

    # Ajustado: usa a constante FAIXA_PH_ADEQUADO[0] em vez de literal mágico 5.5
    if ph < FAIXA_PH_ADEQUADO[0]:
        recomendacoes.append("Aplicar correção da acidez do solo.")

    if FAIXA_FOSFORO_MEDIO[0] <= fosforo <= FAIXA_FOSFORO_MEDIO[1]:
        recomendacoes.append("Melhorar adubação fosfatada.")

    # Ajustado: usa a constante FAIXA_POTASSIO_MEDIO[1] em vez de literal mágico 100
    if potassio > FAIXA_POTASSIO_MEDIO[1]:
        recomendacoes.append("Continuar acompanhando os níveis de potássio.")

    diagnostico["recomendacoes"] = recomendacoes

    return diagnostico


def validar_dados(ph, fosforo, potassio):

    # Ajustado: rejeita bool (pois em Python bool é subclasse de int, ex.: True == 1)
    if isinstance(ph, bool) or not isinstance(ph, (int, float)):
        return False

    if isinstance(fosforo, bool) or not isinstance(fosforo, (int, float)):
        return False

    if isinstance(potassio, bool) or not isinstance(potassio, (int, float)):
        return False

    # Ajustado: limita pH ao intervalo válido [0, 14] e rejeita valores negativos
    if ph < 0 or ph > 14 or fosforo < 0 or potassio < 0:
        return False

    return True