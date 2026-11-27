def formatar_solo(solo_item, indice=None):
    """
    Formata um cadastro de solo para exibição.
    """

    if not isinstance(solo_item, dict):
        return str(solo_item)

    cabecalho = (
        f"Solo #{indice}"
        if indice is not None
        else "Solo"
    )

    propriedade = solo_item.get("propriedade", "Propriedade não informada")

    area = solo_item.get("area", "-")

    area_texto = (
        f"{area:g}"
        if isinstance(area, (int, float))
        else str(area)
    )

    linhas = [
    "",
    "──────────────────────────────────────────────",
    f"◉ ID: {solo_item.get('id', '-')}",
    f"🏠︎ Propriedade: {propriedade}",
    f"⚲ Cidade: {solo_item.get('cidade', '-')}",
    f"⛶ Área (ha): {area_texto}",
    f"𖧧 Cultura: {solo_item.get('cultura', '-')}",
]

    if solo_item.get("criado_em"):
        linhas.append(
            f"• Criado em: {solo_item['criado_em']}"
        )

    linhas.append(
        "=========================================="
    )

    return "\n".join(linhas)


def formatar_perfil(perfil):
    """
    Formata os dados do usuário.
    """

    if not isinstance(perfil, dict):
        return str(perfil)

    linhas = [
    "",
    "══════════════ PERFIL DO USUÁRIO ═════════════",
    f"◉ ID: {perfil.get('id', '-')}",
    f"𐀪 Nome: {perfil.get('nome', '-')}",
    f"✉ E-mail: {perfil.get('email', '-')}",
    "══════════════════════════════════════════════",
]

    return "\n".join(linhas)


def formatar_analise(analise_item, titulo="Análise"):
    """
    Formata uma análise de solo.
    """

    if not isinstance(analise_item, dict):
        return str(analise_item)

    diagnostico = analise_item.get(
        "diagnostico",
        {}
    )

    propriedade = analise_item.get("propriedade", "Propriedade não informada")

    recomendacoes = (
        diagnostico.get("recomendacoes")
        or []
    )

    linhas = [
    "",
    "════════════ ANÁLISE AGRONÔMICA ═════════════",
    f"◉ ID: {analise_item.get('id', '-')}",
    f"🏠︎ Propriedade: {propriedade}",
    f"𖧧 Solo ID: {analise_item.get('solo_id', '-')}",
    "",
    "🗎 DIAGNÓSTICO",
    f"✦ pH: {diagnostico.get('ph')} | Classificação: {diagnostico.get('classificacao_ph')}",
    f"✦ Fósforo: {diagnostico.get('fosforo')} | Prioridade: {diagnostico.get('prioridade_fosforo')}",
    f"✦ Potássio: {diagnostico.get('potassio')} | Prioridade: {diagnostico.get('prioridade_potassio')}",
    "",
    "⚠ RECOMENDAÇÕES",
]

    if recomendacoes:
        linhas.extend(
            f"  - {rec}"
            for rec in recomendacoes
        )
    else:
        linhas.append(
            "  - Nenhuma recomendação adicional no momento."
        )

    linhas.append(
        "=========================================="
    )

    return "\n".join(linhas)