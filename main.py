from entidades import solo, usuario

# Ajustado: import único e limpo de services.analise (regras_diagnostico já é acionado dentro de analise.py)
try:
    from services import analise
except ImportError:
    analise = None


# Ajustado: helper reutilizável para converter números aceitando vírgula ou ponto
def _ler_numero(mensagem):
    return float(input(mensagem).replace(",", ".").strip())


# Ajustado: prioriza a propriedade do solo (com fallbacks) para não exibir "Sem nome"
def _identificar_propriedade(item):
    if not isinstance(item, dict):
        return "Propriedade não informada"
    return (
        item.get("propriedade")
        or item.get("solo_propriedade")
        or item.get("solo_nome")
        or item.get("nome")
        or "Propriedade não informada"
    )


# Ajustado: formata cada solo cadastrado de forma legível na listagem
def _formatar_solo(solo_item, indice=None):
    if not isinstance(solo_item, dict):
        return str(solo_item)

    cabecalho = f"Solo #{indice}" if indice is not None else "Solo"
    propriedade = _identificar_propriedade(solo_item)
    area = solo_item.get("area", "-")
    area_texto = f"{area:g}" if isinstance(area, (int, float)) else str(area)

    linhas = [
        "\n==========================================",
        f"{cabecalho} | ID: {solo_item.get('id', '-')}",
        "------------------------------------------",
        f"• Propriedade: {propriedade}",
        f"• Cidade: {solo_item.get('cidade', '-')}",
        f"• Área: {area_texto}",
        f"• Cultura: {solo_item.get('cultura', '-')}",
    ]
    if solo_item.get("criado_em"):
        linhas.append(f"• Criado em: {solo_item.get('criado_em')}")
    linhas.append("==========================================")
    return "\n".join(linhas)


# Ajustado: formata os dados do perfil do usuário de forma limpa em vez de imprimir o dicionário bruto
def _formatar_perfil(perfil):
    if not isinstance(perfil, dict):
        return str(perfil)

    linhas = [
        "\n==========================================",
        "Perfil do Usuário",
        "------------------------------------------",
        f"• ID: {perfil.get('id', '-')}",
        f"• Nome: {perfil.get('nome', '-')}",
        f"• E-mail: {perfil.get('email', '-')}",
        "==========================================",
    ]
    return "\n".join(linhas)


# Ajustado: formata o resultado da análise de forma reutilizável para criação, listagem, consulta e atualização
def _formatar_analise(analise_item, titulo="Análise"):
    diag = analise_item.get("diagnostico", {})
    # Ajustado: exibe a propriedade vinculada à análise em vez de depender de "solo_nome" / "Sem nome"
    propriedade_solo = _identificar_propriedade(analise_item)
    solo_id = analise_item.get("solo_id", "-")
    recomendacoes = diag.get("recomendacoes") or []

    linhas = [
        "\n==========================================",
        f"{titulo} | ID: {analise_item.get('id', '-')}",
        f"Propriedade: {propriedade_solo} (Solo ID: {solo_id})",
        "------------------------------------------",
        f"• pH: {diag.get('ph')}  |  Classificação: {diag.get('classificacao_ph')}",
        f"• Fósforo: {diag.get('fosforo')}  |  Prioridade: {diag.get('prioridade_fosforo')}",
        f"• Potássio: {diag.get('potassio')}  |  Prioridade: {diag.get('prioridade_potassio')}",
        "------------------------------------------",
        "Recomendações:",
    ]

    if recomendacoes:
        for rec in recomendacoes:
            linhas.append(f"  - {rec}")
    else:
        linhas.append("  - Nenhuma recomendação adicional no momento.")

    linhas.append("==========================================")
    return "\n".join(linhas)


def menu_solo(user):
    uid = user["id"]
    while True:
        print("\n--- SOLO ---")
        print("1 - Cadastrar solo")
        print("2 - Listar solos")
        print("3 - Consultar por ID")
        print("4 - Atualizar")
        print("5 - Excluir")
        print("0 - Voltar")
        op = input("Opção: ").strip()

        try:
            # Ajustado: solo agora cadastra apenas dados do terreno (sem pH, fósforo e potássio)
            if op == "1":
                s = solo.cadastrar_solo(
                    uid,
                    propriedade=input("Propriedade: "),
                    cidade=input("Cidade: "),
                    area=_ler_numero("Área: "),
                    cultura=input("Cultura: "),
                )
                print("Criado! ID:", s["id"])
            elif op == "2":
                # Ajustado: formata cada solo listado e trata lista vazia
                solos = solo.listar_solos(uid)
                if not solos:
                    print("Nenhum solo cadastrado.")
                else:
                    for idx, item in enumerate(solos, start=1):
                        print(_formatar_solo(item, indice=idx))
            elif op == "3":
                print(solo.consultar_solo(uid, input("ID: ").strip()))
            elif op == "4":
                sid = input("ID: ").strip()
                solo.atualizar_solo(
                    uid,
                    sid,
                    propriedade=input("Propriedade: "),
                    cidade=input("Cidade: "),
                    area=_ler_numero("Área: "),
                    cultura=input("Cultura: "),
                )
                print("Atualizado!")
            elif op == "5":
                solo.excluir_solo(uid, input("ID: ").strip())
                print("Excluído!")
            elif op == "0":
                break
            else:
                print("Opção inválida.")
        except Exception as e:
            print("Erro:", e)


# Ajustado: recebe user para listar/selecionar o solo do usuário e vincular a análise ao solo escolhido
def menu_analise(user):
    if not analise:
        print("Módulo de análise indisponível.")
        return

    uid = user["id"]
    while True:
        print("\n--- ANÁLISE ---")
        print("1 - Gerar e salvar")
        print("2 - Listar")
        print("3 - Consultar por ID")
        print("4 - Atualizar por ID")
        print("5 - Excluir por ID")
        print("0 - Voltar")
        op = input("Opção: ").strip()

        try:
            if op == "1":
                solos = solo.listar_solos(uid)
                if not solos:
                    print("Cadastre um solo antes de solicitar uma análise.")
                    continue

                print("\nSolos disponíveis:")
                for s in solos:
                    # Ajustado: exibe a propriedade do solo em vez de "Nome: Sem nome"
                    propriedade_solo = _identificar_propriedade(s)
                    print(
                        f"- ID: {s.get('id', '-')} | "
                        f"Propriedade: {propriedade_solo} | "
                        f"Cidade: {s.get('cidade', '-')} | "
                        f"Cultura: {s.get('cultura', '-')}"
                    )

                # Ajustado: solicita qual solo será analisado antes de pedir pH, fósforo e potássio
                solo_id = input("Informe o ID do solo desejado: ").strip()
                solo.consultar_solo(uid, solo_id)

                ph = _ler_numero("pH: ")
                fosforo = _ler_numero("Fósforo: ")
                potassio = _ler_numero("Potássio: ")

                criada = analise.cadastrar_analise(uid, solo_id, ph, fosforo, potassio)
                # Ajustado: exibe a análise formatada em vez do dicionário bruto
                print(_formatar_analise(criada, titulo="Análise criada com sucesso!"))
            elif op == "2":
                # Ajustado: formata cada item da listagem e informa quando não houver análises
                analises = analise.listar_analises(uid)
                if not analises:
                    print("Nenhuma análise cadastrada.")
                else:
                    for item in analises:
                        print(_formatar_analise(item, titulo="Análise"))
            elif op == "3":
                aid = input("ID da análise: ").strip()
                consultada = analise.consultar_analise(uid, aid)
                # Ajustado: exibe a análise consultada no mesmo padrão formatado
                print(_formatar_analise(consultada, titulo="Consulta de Análise"))
            elif op == "4":
                aid = input("ID da análise: ").strip()
                ph = _ler_numero("Novo pH: ")
                fosforo = _ler_numero("Novo Fósforo: ")
                potassio = _ler_numero("Novo Potássio: ")
                atualizada = analise.atualizar_analise(uid, aid, ph, fosforo, potassio)
                # Ajustado: exibe a análise atualizada no mesmo padrão formatado
                print(_formatar_analise(atualizada, titulo="Análise atualizada!"))
            elif op == "5":
                aid = input("ID da análise: ").strip()
                analise.excluir_analise(uid, aid)
                print("Análise excluída!")
            elif op == "0":
                break
            else:
                print("Opção inválida.")
        except Exception as e:
            print("Erro:", e)


def menu_logado(user):
    while True:
        print(f"\n=== G.A.L.O. | Olá {user['nome']}, o que podemos ajudar? ===")
        print("1 - Solos")
        print("2 - Análise")
        print("3 - Ver perfil")
        print("4 - Atualizar perfil")
        print("5 - Excluir conta")
        print("0 - Sair")
        op = input("Opção: ").strip()

        try:
            if op == "1":
                menu_solo(user)
            elif op == "2":
                # Ajustado: passa user para menu_analise
                menu_analise(user)
            elif op == "3":
                # Ajustado: exibe o perfil do usuário formatado
                perfil_atual = usuario.consultar_usuario(user["id"])
                print(_formatar_perfil(perfil_atual))
            elif op == "4":
                user = usuario.atualizar_usuario(
                    user["id"],
                    input("Novo nome: "),
                    input("Novo e-mail: "),
                    input("Senha atual: "),
                    input("Nova senha (ou ENTER): ") or None,
                )
                print("Atualizado!")
            elif op == "5":
                usuario.excluir_usuario(user["id"], input("Senha: "))
                print("Conta excluída!")
                break
            elif op == "0":
                break
            else:
                print("Opção inválida.")
        except Exception as e:
            print("Erro:", e)


def main():
    while True:
        print("\n=== G.A.L.O. ===")
        print("1 - Login")
        print("2 - Cadastrar usuário")
        print("0 - Sair")
        op = input("Opção: ").strip()

        try:
            if op == "1":
                user = usuario.autenticar(
                    input("E-mail: "),
                    input("Senha: "),
                )
                if user:
                    menu_logado(user)
                else:
                    print("Login inválido.")
            elif op == "2":
                user = usuario.cadastrar_usuario(
                    input("Nome: "),
                    input("E-mail: "),
                    input("Senha: "),
                )
                print("Cadastrado! ID:", user["id"])
            elif op == "0":
                break
            else:
                print("Opção inválida.")
        except Exception as e:
            print("Erro:", e)


if __name__ == "__main__":
    main()