import json

def consultar_db(db):
    """
    Retorna uma consulta no json escolhido pelo cliente\n
    PARAMS:
    db - nome do arquivo json - str\n
    RETURNS:
    json.load - listagem da consulta realizada - dict
    none - retorno da exceção - none
    """
    try:
        with open(f"database/{db}.json", "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception as e:
        print(f"Erro ao carregar {db}: {e}")
        return None


def salvar_db(db, dados):
    """
    Salva no banco de dados as entradas do cliente
    PARAMS:
    db - nome do arquivo json - string\n
    dados - dict dos dados do cliente
    RETURNS:
    true - significa que salvou os dados no db com sucesso - boolean
    false - retorno da exceção - boolean
    """
    try:
        with open(f"database/{db}.json", "w", encoding="utf-8") as f:
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