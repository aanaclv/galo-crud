import json

def consultar_db(db):
    try:
        with open(f"database/{db}.json","r",encoding="utf-8") as f:
            return json.load(f)

    except Exception as e:
        print(f"Erro ao carregar {db}: {e}")
        return None

    banco = consultar_db("db_usuario")

    if banco is None:
        return "Erro ao acessar o banco."


def salvar_db(db, dados):
    try:
        with open(f"database/{db}.json","w", encoding="utf-8") as f:
            json.dump(
                dados,
                f,
                ensure_ascii=False,
                indent=4
            )

            return True
    except Exception as e:
        print(f"Erro ao salvar {db}: {e}")
        return False