from entidades import solo, usuario

try:
    from services import analise
except ImportError:
    analise = None



from ui.formatadores import (
    formatar_numero,
    formatar_solo,
    formatar_perfil,
    formatar_analise,
)

def menu_principal():

    while True:

        print(r"""
       ,~.
    ,-'__ `-,
   {,-'  `. }              ,')
  ,( a )   `-.__         ,',')~,
 <=.) (         `-.__,==' ' ' '}
   (   )                      /
    `-'\   ,                    )
        |  \        `~.        /
        \   `._        \      /
         \     `._____,'    ,'
          `-.             ,'
             `-._     _,-'
                 77jj'
                //_||
             __//--'/`
           ,--'/`  '
                """)

        print("\n┌──────────────────────────────────────────┐")
        print("│      G.A.L.O. - Sistema Agrícola         │")
        print("└──────────────────────────────────────────┘")

        print("\n1. Login")
        print("2. Cadastrar usuário")
        print("0. Sair")

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


def menu_logado(user):

    while True:

        print("\n╔══════════════════════════════════════════════╗")
        print("║      G.A.L.O. - Gestão Agrícola Online      ║")
        print("╚══════════════════════════════════════════════╝")

        print(f"\nOlá, {user['nome']}! ☀")
        print("Como podemos ajudar hoje?\n")

        print("➤ Gestão de Solos")
        print("  [1] - Consultar solos")
        print("  [2] - Consultar análises")

        print("\n➤ Minha Conta")
        print("  [3] - Ver perfil")
        print("  [4] - Atualizar perfil")
        print("  [5] - Excluir conta")

        print("\n➤ Sistema")
        print("  [0] - Sair")

        print("\n" + "─" * 46)

        op = input("Opção: ").strip()

        try:

            if op == "1":

                menu_solo(user)

            elif op == "2":

                menu_analise(user)

            elif op == "3":

                perfil = usuario.consultar_usuario(
                    user["id"]
                )

                print(
                    formatar_perfil(perfil)
                )

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

                usuario.excluir_usuario(
                    user["id"],
                    input("Senha: ")
                )

                print("Conta excluída!")
                break

            elif op == "0":

                break

            else:

                print("Opção inválida.")

        except Exception as e:

            print("Erro:", e)

def menu_solo(user):

    uid = user["id"]

    while True:

        print("\n╔══════════════════════════════════════════════╗")
        print("║            ☘ GESTÃO DE SOLOS ☘              ║")
        print("╚══════════════════════════════════════════════╝")

        print("\nOperações Disponíveis")
        print("  [1] Cadastrar solo")
        print("  [2] Listar solos cadastrados")
        print("  [3] Consultar solo por ID")
        print("  [4] Atualizar dados do solo")
        print("  [5] Excluir registro")

        print("\n↩ Navegação")
        print("  [0] Voltar ao menu principal")

        print("\n" + "─" * 46)

        op = input("Opção: ").strip()

        try:

            if op == "1":

                s = solo.cadastrar_solo(
                    uid,
                    propriedade=input("Propriedade: "),
                    cidade=input("Cidade: "),
                    area=formatar_numero("Área (ha): "),
                    cultura=input("Cultura: "),
                )

                print("Criado! ID:", s["id"])

            elif op == "2":

                solos = solo.listar_solos(uid)

                if not solos:

                    print("Nenhum solo cadastrado.")

                else:

                    for idx, item in enumerate(
                        solos,
                        start=1
                    ):
                        print(
                            formatar_solo(
                                item,
                                indice=idx
                            )
                        )

            elif op == "3":

                resultado = solo.consultar_solo(
                    uid,
                    input("ID: ").strip()
                )

                print(resultado)

            elif op == "4":

                sid = input("ID: ").strip()

                solo.atualizar_solo(
                    uid,
                    sid,
                    propriedade=input("Propriedade: "),
                    cidade=input("Cidade: "),
                    area=formatar_numero("Área (ha): "),
                    cultura=input("Cultura: "),
                )

                print("Atualizado!")

            elif op == "5":

                solo.excluir_solo(
                    uid,
                    input("ID: ").strip()
                )

                print("Excluído!")

            elif op == "0":

                break

            else:

                print("Opção inválida.")

        except Exception as e:

            print("Erro:", e)

def menu_analise(user):

    if not analise:
        print("Módulo de análise indisponível.")
        return

    uid = user["id"]

    while True:

        print("\n╔══════════════════════════════════════════════╗")
        print("║           ✦ MÓDULO DE ANÁLISES ✦            ║")
        print("╚══════════════════════════════════════════════╝")

        print("\nSelecione uma operação:\n")

        print("∎ [1] Gerar nova análise")
        print("∎ [2] Listar análises")
        print("∎ [3] Consultar análise por ID")
        print("∎  [4] Atualizar análise")
        print("∎  [5] Excluir análise")
        print("↩  [0] Retornar ao menu principal")

        print("\n" + "─" * 46)

        op = input("Opção: ").strip()

        try:

            if op == "1":

                solos = solo.listar_solos(uid)

                if not solos:
                    print(
                        "Cadastre um solo antes de solicitar uma análise."
                    )
                    continue

                print("\nSolos disponíveis:")

                for s in solos:

                    print("\n──────────────────────────────────────────────")
                    print(f"◉ ID: {s.get('id')}")
                    print(f"🏠︎ Propriedade: {s.get('propriedade', '-')}")
                    print(f"⚲ Cidade: {s.get('cidade', '-')}")
                    print(f"𖧧 Cultura: {s.get('cultura', '-')}")

                solo_id = input(
                    "Informe o ID do solo desejado: "
                ).strip()

                solo.consultar_solo(
                    uid,
                    solo_id
                )

                ph = formatar_numero("pH (5.5 - 7.0): ")
                fosforo = formatar_numero("Fósforo (mg/dm³) (10 - 20): ")
                potassio = formatar_numero("Potássio (cmolc/dm³) (50 - 100): ")

                criada = analise.cadastrar_analise(
                    uid,
                    solo_id,
                    ph,
                    fosforo,
                    potassio
                )

                print(
                    formatar_analise(
                        criada,
                        "Análise criada com sucesso!"
                    )
                )

            elif op == "2":

                analises = (
                    analise.listar_analises(uid)
                )

                if not analises:

                    print(
                        "Nenhuma análise cadastrada."
                    )

                else:

                    for item in analises:

                        print(
                            formatar_analise(
                                item
                            )
                        )

            elif op == "3":

                aid = input(
                    "ID da análise: "
                ).strip()

                consulta = (
                    analise.consultar_analise(
                        uid,
                        aid
                    )
                )

                print(
                    formatar_analise(
                        consulta,
                        "Consulta de Análise"
                    )
                )

            elif op == "4":

                aid = input(
                    "ID da análise: "
                ).strip()

                ph = formatar_numero("Novo pH: ")
                fosforo = formatar_numero(
                    "Novo Fósforo: "
                )
                potassio = formatar_numero(
                    "Novo Potássio: "
                )

                atualizada = (
                    analise.atualizar_analise(
                        uid,
                        aid,
                        ph,
                        fosforo,
                        potassio
                    )
                )

                print(
                    formatar_analise(
                        atualizada,
                        "Análise atualizada!"
                    )
                )

            elif op == "5":

                aid = input(
                    "ID da análise: "
                ).strip()

                analise.excluir_analise(
                    uid,
                    aid
                )

                print("Análise excluída!")

            elif op == "0":

                break

            else:

                print("Opção inválida.")

        except Exception as e:

            print("Erro:", e)