import os
import json


PASTA_JOGADORES = "Jogadores"

def caminho_arquivo(id_jogador, nome_personagem):
    id_str = str(id_jogador)
    caminho_pasta_usuario = os.path.join(PASTA_JOGADORES, id_str)

    if not os.path.exists(caminho_pasta_usuario):
        os.makedirs(caminho_pasta_usuario)

    nome_arquivo = f"{nome_personagem}.json"
    caminho = os.path.join(caminho_pasta_usuario, nome_arquivo)
    return caminho

def salvar_personagem(id_jogador, nome_personagem, dados_jogador):
    caminho = caminho_arquivo(id_jogador, nome_personagem)

    if not os.path.exists(PASTA_JOGADORES):
        os.makedirs(PASTA_JOGADORES) #mkdir topdms

    with open(caminho, "w", encoding= "utf-8") as arquivo:
        json.dump(dados_jogador, arquivo, indent=4, ensure_ascii= False) #o .dump é um tradutor para JSON, e depois 'despeja' no arquivo que abrimos. basicamente funciona assim: dicionario -> Json

def carregar_personagem(id_jogador, nome_personagem):
    caminho = caminho_arquivo(id_jogador, nome_personagem)
    if os.path.exists(caminho):
        with open(caminho, "r" , encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            return dados
        
    else:
        return None
    
def deletar_personagem(id_jogador, nome_personagem):
    caminho = caminho_arquivo(id_jogador, nome_personagem)
    if os.path.exists(caminho):
        os.remove(caminho)
        return True
    else:
        return False

def personagem_existe(id_jogador, nome_personagem):
    caminho = caminho_arquivo(id_jogador, nome_personagem)

    if os.path.exists(caminho):
        return True
    else:
        return False
    
def listar_personagens(id_jogador):
    caminho = os.path.join(PASTA_JOGADORES, str(id_jogador))

    lista_nomes = []
    if os.path.exists(caminho):
        arquivos = os.listdir(caminho)
        for arquivo in arquivos:
            if arquivo.endswith(".json"):
                nome_limpo = arquivo.replace(".json", "")
                lista_nomes.append(nome_limpo)

    return lista_nomes

def renomear_personagem(id_jogador, nome_antigo, nome_novo):
    caminho_antigo = caminho_arquivo(id_jogador, nome_antigo)
    caminho_novo = caminho_arquivo(id_jogador, nome_novo)
    
    if not os.path.exists(caminho_antigo):
        return False, "Personagem antigo não encontrado."

    if os.path.exists(caminho_novo):
        return False, "Já existe um personagem com esse novo nome."

    dados = carregar_personagem(id_jogador, nome_antigo)
    dados["nome"] = nome_novo 
    
    salvar_personagem(id_jogador, nome_novo, dados)
    
    os.remove(caminho_antigo)
    
    return True, "Sucesso"

def editar_atributo_personagem(id_jogador, nome_personagem, atributo, novo_valor):
    dados = carregar_personagem(id_jogador, nome_personagem)
    
    if dados:
        atributo = atributo.lower()
        
        if atributo in dados["atributos"]:
            try:
                dados["atributos"][atributo] = int(novo_valor)
                salvar_personagem(id_jogador, nome_personagem, dados)
                return True, f"{atributo} alterado para {novo_valor}."
            except ValueError:
                return False, "O valor do atributo precisa ser um número inteiro."
        else:
            return False, f"Atributo '{atributo}' não encontrado na ficha."
    else:
        return False, "Personagem não encontrado."