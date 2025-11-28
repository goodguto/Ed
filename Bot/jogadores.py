import os
import json


PASTA_JOGADORES = "Jogadores"

def caminho_arquivo(id_jogador):
    nome_arquivo = f"{str(id_jogador)}.json" # a ficha do jogador
    caminho = os.path.join(PASTA_JOGADORES, nome_arquivo)
    return caminho

def salvar_jogador(id_jogador, dados_jogador):
    caminho = caminho_arquivo(id_jogador)

    if not os.path.exists(PASTA_JOGADORES):
        os.makedirs(PASTA_JOGADORES) #mkdir topdms

    with open(caminho, "w", encoding= "utf-8") as arquivo:
        json.dump(dados_jogador, arquivo, indent=4, ensure_ascii= False) #o .dump é um tradutor para JSON, e depois 'despeja' no arquivo que abrimos. basicamente funciona assim: dicionario -> Json

def carregar_jogador(id_jogador):
    caminho = caminho_arquivo(id_jogador)
    if os.path.exists(caminho):
        with open(caminho, "r" , encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            return dados
        
    else:
        return None
    
def deletar_jogador(id_jogador):
    caminho = caminho_arquivo(id_jogador)
    if os.path.exists(caminho):
        os.remove(caminho)
        return True
    else:
        return False

def jogador_existe(id_jogador):
    caminho = caminho_arquivo(id_jogador)

    if os.path.exists(caminho):
        return True
    else:
        return False