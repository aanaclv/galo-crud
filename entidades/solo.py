import math
import secrets
from datetime import datetime

# Ajustado: trocou o import comentado de armazenamento pelo db.py
from db import consultar_db, salvar_db
# Ajustado: removido import de gerar_diagnostico; a análise de pH, fósforo e potássio fica em analise.py / regras_diagnostico.py

# Ajustado: usa o nome base sem ".json", pois db.py monta "database/<db>.json"
DB_SOLO = "db_solo"


# Ajustado: incluída validação de texto pois antes dependia de "from .armazenamento import ... texto"
def texto(valor, campo):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"{campo}: informe um texto válido.")
    return valor.strip()


# Ajustado: garante sempre uma list de solos mesmo se vier dict, None ou str
def _carregar_solos():
    dados = consultar_db(DB_SOLO)
    if isinstance(dados, list):
        return dados
    if isinstance(dados, dict):
        for chave in ("solo", "solos", "diagnosticos"):
            if isinstance(dados.get(chave), list):
                return dados[chave]
    return []


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


# Ajustado: removidas FAIXA_*, prioridade_nutriente e analisar_solo para manter as regras apenas em regras_diagnostico.py
# Ajustado: removidos ph, fosforo, potassio e resultado/gerar_diagnostico de validar_dados (agora pertencem à análise)
# Validação dos dados do solo
def validar_dados(
    propriedade, cidade, area, cultura
):
    # Ajustado: mantido o campo "nome" na assinatura e no dicionário para compatibilidade com o cadastro/menu
    dados = {
        "propriedade": texto(propriedade, "Propriedade"),
        "cidade": texto(cidade, "Cidade"),
        "area": numero(area, "Área", positivo=True),
        "cultura": texto(cultura, "Cultura")
    }

    return dados


# CREATE - Cadastrar solo
def cadastrar_solo(usuario_id, **dados):
    from .usuario import consultar_usuario

    consultar_usuario(usuario_id)

    # Ajustado: usa _carregar_solos() para evitar erro quando consultar_db retorna dict/None/str
    solos = _carregar_solos()

    solo_item = {
        "id": secrets.token_hex(8),
        "usuario_id": usuario_id,
        "criado_em": datetime.now().isoformat(
            timespec="seconds"
        )
    }

    solo_item.update(validar_dados(**dados))

    solos.append(solo_item)
    # Ajustado: usa salvar_db com o nome base DB_SOLO
    salvar_db(DB_SOLO, solos)

    return solo_item


# READ - Listar solos
def listar_solos(usuario_id):
    # Ajustado: usa _carregar_solos() e protege contra itens não-dict
    solos = _carregar_solos()
    return [
        s for s in solos
        if isinstance(s, dict) and s.get("usuario_id") == usuario_id
    ]


# READ - Consultar solo específico
def consultar_solo(usuario_id, solo_id):
    for solo_item in listar_solos(usuario_id):

        if solo_item["id"] == solo_id:
            return solo_item

    raise ValueError("Solo não encontrado.")


# UPDATE - Atualizar solo
def atualizar_solo(
    usuario_id, solo_id, **dados
):
    # Ajustado: usa _carregar_solos()
    solos = _carregar_solos()

    for solo_item in solos:

        if (
            isinstance(solo_item, dict)
            and solo_item.get("usuario_id") == usuario_id
            and solo_item.get("id") == solo_id
        ):
            solo_item.update(validar_dados(**dados))

            solo_item["atualizado_em"] = (
                datetime.now().isoformat(timespec="seconds")
            )

            # Ajustado: usa salvar_db com o nome base DB_SOLO
            salvar_db(DB_SOLO, solos)

            return solo_item

    raise ValueError("Solo não encontrado.")


# DELETE - Excluir solo
def excluir_solo(usuario_id, solo_id):
    # Ajustado: verifica se existem análises vinculadas a este solo antes de excluir
    try:
        from services.analise import listar_analises
        if any(a.get("solo_id") == solo_id for a in listar_analises(usuario_id)):
            raise ValueError(
                "Exclua as análises vinculadas a este solo antes de excluí-lo."
            )
    except ImportError:
        pass

    # Ajustado: usa _carregar_solos()
    solos = _carregar_solos()

    for solo_item in solos:

        if (
            isinstance(solo_item, dict)
            and solo_item.get("usuario_id") == usuario_id
            and solo_item.get("id") == solo_id
        ):
            solos.remove(solo_item)
            # Ajustado: usa salvar_db com o nome base DB_SOLO
            salvar_db(DB_SOLO, solos)

            return

    raise ValueError("Solo não encontrado.")