def ler_numero(mensagem):
    return float(input(mensagem).replace(",", ".").strip())


def identificar_propriedade(item):
    if not isinstance(item, dict):
        return "Propriedade não informada"

    return (
        item.get("propriedade")
        or item.get("solo_propriedade")
        or item.get("solo_nome")
        or item.get("nome")
        or "Propriedade não informada"
    )