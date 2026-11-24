import math
import secrets
from datetime import datetime
from .armazenamento import carregar, salvar, texto

ARQUIVO = "db_solo.json"

FAIXA_PH = (5.5, 7.0)
FAIXA_P = (10, 20)
FAIXA_K = (50, 100)


# Validação de valores numéricos
def numero(valor, campo, minimo=0, maximo=None, positivo=False):
    try:
        valor = float(str(valor).replace(",", "."))

    except (ValueError, TypeError):
        raise ValueError(
            f"{campo}: informe um número válido."
        ) from None

    if (
        not math.isfinite(valor)
        or valor < minimo
        or (positivo and valor == 0)
        or (maximo is not None and valor > maximo)
    ):
        raise ValueError(
            f"{campo}: valor fora da faixa permitida."
        )

    return valor


# Classificação das prioridades
def prioridade_nutriente(valor, faixa):
    if valor < faixa[0]:
        return "ALTA"

    elif valor <= faixa[1]:
        return "MÉDIA"

    else:
        return "BAIXA"


# Análise de pH, fósforo e potássio
def analisar_solo(ph, fosforo, potassio):
    ph = numero(ph, "pH", maximo=14)
    fosforo = numero(fosforo, "Fósforo")
    potassio = numero(potassio, "Potássio")

    # Avaliação do pH
    if ph < FAIXA_PH[0]:
        classe_ph = "Solo ácido"
        prioridade_ph = "ALTA"
        rec_ph = (
            "Avaliar a necessidade de correção da acidez "
            "com assistência técnica."
        )

    elif ph <= FAIXA_PH[1]:
        classe_ph = "Solo adequado"
        prioridade_ph = "BAIXA"
        rec_ph = "Continuar monitorando o pH."

    else:
        classe_ph = "Solo alcalino"
        prioridade_ph = "ALTA"
        rec_ph = (
            "Investigar a alcalinidade com assistência técnica."
        )

    # Avaliação do fósforo e potássio
    p = prioridade_nutriente(fosforo, FAIXA_P)
    k = prioridade_nutriente(potassio, FAIXA_K)

    recomendacoes_p = {
        "ALTA": "Avaliar a necessidade de adubação fosfatada.",
        "MÉDIA": "Revisar o manejo do fósforo.",
        "BAIXA": "Monitorar os níveis de fósforo."
    }

    recomendacoes_k = {
        "ALTA": "Avaliar a necessidade de adubação potássica.",
        "MÉDIA": "Revisar o manejo do potássio.",
        "BAIXA": "Monitorar os níveis de potássio."
    }

    return {
        "ph": {
            "diagnostico": classe_ph,
            "prioridade": prioridade_ph,
            "recomendacao": rec_ph
        },
        "fosforo": {
            "prioridade": p,
            "recomendacao": recomendacoes_p[p]
        },
        "potassio": {
            "prioridade": k,
            "recomendacao": recomendacoes_k[k]
        }
    }


# Validação dos dados do diagnóstico
def validar_dados(
    nome, propriedade, cidade, area,
    cultura, ph, fosforo, potassio
):
    dados = {
        "nome": texto(nome, "Nome"),
        "propriedade": texto(propriedade, "Propriedade"),
        "cidade": texto(cidade, "Cidade"),
        "area": numero(area, "Área", positivo=True),
        "cultura": texto(cultura, "Cultura"),
        "ph": numero(ph, "pH", maximo=14),
        "fosforo": numero(fosforo, "Fósforo"),
        "potassio": numero(potassio, "Potássio")
    }

    dados["resultado"] = analisar_solo(
        dados["ph"],
        dados["fosforo"],
        dados["potassio"]
    )

    return dados


# CREATE - Cadastrar diagnóstico do solo
def cadastrar_diagnostico(usuario_id, **dados):
    from .usuario import consultar_usuario

    consultar_usuario(usuario_id)

    diagnosticos = carregar(ARQUIVO)

    diagnostico = {
        "id": secrets.token_hex(8),
        "usuario_id": usuario_id,
        "criado_em": datetime.now().isoformat(
            timespec="seconds"
        )
    }

    diagnostico.update(validar_dados(**dados))

    diagnosticos.append(diagnostico)
    salvar(ARQUIVO, diagnosticos)

    return diagnostico


# READ - Listar diagnósticos
def listar_diagnosticos(usuario_id):
    return [
        d for d in carregar(ARQUIVO)
        if d["usuario_id"] == usuario_id
    ]


# READ - Consultar diagnóstico específico
def consultar_diagnostico(usuario_id, diagnostico_id):
    for diagnostico in listar_diagnosticos(usuario_id):

        if diagnostico["id"] == diagnostico_id:
            return diagnostico

    raise ValueError("Diagnóstico não encontrado.")


# UPDATE - Atualizar diagnóstico
def atualizar_diagnostico(
    usuario_id, diagnostico_id, **dados
):
    diagnosticos = carregar(ARQUIVO)

    for diagnostico in diagnosticos:

        if (
            diagnostico["usuario_id"] == usuario_id
            and diagnostico["id"] == diagnostico_id
        ):
            diagnostico.update(validar_dados(**dados))

            diagnostico["atualizado_em"] = (
                datetime.now().isoformat(timespec="seconds")
            )

            salvar(ARQUIVO, diagnosticos)

            return diagnostico

    raise ValueError("Diagnóstico não encontrado.")


# DELETE - Excluir diagnóstico
def excluir_diagnostico(usuario_id, diagnostico_id):
    diagnosticos = carregar(ARQUIVO)

    for diagnostico in diagnosticos:

        if (
            diagnostico["usuario_id"] == usuario_id
            and diagnostico["id"] == diagnostico_id
        ):
            diagnosticos.remove(diagnostico)
            salvar(ARQUIVO, diagnosticos)

            return

    raise ValueError("Diagnóstico não encontrado.")