import json


def consultar_db(db): 
    print(f"Você está utilizando o banco de dados {db}")
    try:
        
        with open(f"database/{db}.json", "r", encoding="utf-8") as f:
            banco = json.load(f)

        return banco
    except Exception as e:
        return f"Ocorreu um problema, o banco de dados não possui a estrutura básica JSON para realizar consultas: {e}"


def cadastrar_usuario(nome, email, senha, id):

    banco = consultar_db("db_usuario")

    novo_id = len(banco["user"]) + 1

    usuario = {
        "id": novo_id,
        "nome": nome,
        "email": email,
        "senha": senha,
    }

    banco["user"].append(usuario)
    try:
        with open("database/db_usuario.json", "w", encoding="utf-8") as f:
            json.dump(banco, f,indent=4, ensure_ascii=False)

        return f"Usuário {usuario['nome']} cadastrado com sucesso."
    except Exception as e:
        return f"Ocorreu um problema: {e}"


def cadastrar_solo(propriedade, cidade, area, plantacao):

    banco = consultar_db("db_solo")

    solo = {
        "propriedade": propriedade,
        "cidade": cidade,
        "area": area,
        "plantacao": plantacao
    }

    banco["solo"].append(solo)
    try:
       with open("database/db_solo.json", "w", encoding="utf-8") as f:
            json.dump(banco, f, ensure_ascii=False, indent=4)
            return f"Solo da propriedade {solo['propriedade']} cadastrado com sucesso." 
    
    except Exception as e:
            return f"Ocorreu um problema: {e}"



