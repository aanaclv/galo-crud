import math
import secrets
from datetime import datetime

# Ajustado: usa db.py com nome base sem ".json" ("database/db_analise.json")
from db import consultar_db, salvar_db
from entidades.solo import consultar_solo
from services.regras_diagnostico import gerar_diagnostico

DB_ANALISE = "db_analise"


# Ajustado: centraliza a resolução da propriedade do solo para evitar "Sem nome" e KeyError
def _obter_propriedade_solo(solo_dict):
    if not isinstance(solo_dict, dict):
        return "Propriedade não informada"
    return (
        solo_dict.get("propriedade")
        or solo_dict.get("nome")
        or "Propriedade não informada"
    )


# Ajustado: normaliza números (aceita vírgula ou ponto) antes de repassar a gerar_diagnostico
def _normalizar_parametro(valor, campo):
    if isinstance(valor, bool):
        raise ValueError(f"{campo}: informe um número válido.")
    try:
        numero = float(str(valor).replace(",", ".").strip())
    except (ValueError, TypeError):
        raise ValueError(f"{campo}: informe um número válido.") from None

    if not math.isfinite(numero):
        raise ValueError(f"{campo}: informe um número válido.")

    return numero


# Ajustado: garante sempre uma list de análises mesmo se consultar_db retornar dict, None ou str
def _carregar_analises():
    dados = consultar_db(DB_ANALISE)
    if isinstance(dados, list):
        return dados
    if isinstance(dados, dict):
        for chave in ("analise", "analises"):
            if isinstance(dados.get(chave), list):
                return dados[chave]
    return []


# Ajustado: exige um solo válido do usuário, normaliza pH/fósforo/potássio e aplica regras_diagnostico
def cadastrar_analise(usuario_id, solo_id, ph, fosforo, potassio):
    solo_selecionado = consultar_solo(usuario_id, solo_id)

    ph_num = _normalizar_parametro(ph, "pH")
    fosforo_num = _normalizar_parametro(fosforo, "Fósforo")
    potassio_num = _normalizar_parametro(potassio, "Potássio")

    resultado = gerar_diagnostico(ph_num, fosforo_num, potassio_num)

    # Ajustado: puxa a propriedade do solo selecionado em vez de depender apenas de "nome"
    propriedade_solo = _obter_propriedade_solo(solo_selecionado)

    analises = _carregar_analises()
    analise_item = {
        "id": secrets.token_hex(8),
        "usuario_id": usuario_id,
        "solo_id": solo_selecionado["id"],
        "propriedade": propriedade_solo,
        # Ajustado: mantém "solo_nome" preenchido com a propriedade para compatibilidade com leituras existentes
        "solo_nome": propriedade_solo,
        "criado_em": datetime.now().isoformat(timespec="seconds"),
        "diagnostico": resultado,
    }

    analises.append(analise_item)
    salvar_db(DB_ANALISE, analises)
    return analise_item


# Ajustado: filtra apenas registros dict pertencentes ao usuario_id
def listar_analises(usuario_id):
    return [
        a for a in _carregar_analises()
        if isinstance(a, dict) and a.get("usuario_id") == usuario_id
    ]


def consultar_analise(usuario_id, analise_id):
    for a in listar_analises(usuario_id):
        if a.get("id") == analise_id:
            return a
    raise ValueError("Análise não encontrada.")


# Ajustado: revalida/normaliza pH, fósforo e potássio na atualização e verifica se o solo ainda existe
def atualizar_analise(usuario_id, analise_id, ph, fosforo, potassio):
    ph_num = _normalizar_parametro(ph, "pH")
    fosforo_num = _normalizar_parametro(fosforo, "Fósforo")
    potassio_num = _normalizar_parametro(potassio, "Potássio")

    analises = _carregar_analises()
    for a in analises:
        if (
            isinstance(a, dict)
            and a.get("usuario_id") == usuario_id
            and a.get("id") == analise_id
        ):
            if a.get("solo_id"):
                solo_atual = consultar_solo(usuario_id, a["solo_id"])
                # Ajustado: atualiza "propriedade" e "solo_nome" com a propriedade atual do solo vinculado
                propriedade_atual = _obter_propriedade_solo(solo_atual)
                a["propriedade"] = propriedade_atual
                a["solo_nome"] = propriedade_atual

            a["diagnostico"] = gerar_diagnostico(ph_num, fosforo_num, potassio_num)
            a["atualizado_em"] = datetime.now().isoformat(timespec="seconds")
            salvar_db(DB_ANALISE, analises)
            return a
    raise ValueError("Análise não encontrada.")


def excluir_analise(usuario_id, analise_id):
    analises = _carregar_analises()
    for a in analises:
        if (
            isinstance(a, dict)
            and a.get("usuario_id") == usuario_id
            and a.get("id") == analise_id
        ):
            analises.remove(a)
            salvar_db(DB_ANALISE, analises)
            return
    raise ValueError("Análise não encontrada.")