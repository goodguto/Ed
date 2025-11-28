import os
import discord

intents = discord.Intents.default()
intents.message_content = True

Cliente = discord.Client(intents=intents)

def carregar_token():
    token_lido= ""
    if os.path.exists("token.txt"):
        with open("token.txt", "r") as arquivo:
            conteudo = arquivo.read()
            token_lido = conteudo.strip()
    else:
        print("ERRO: o arquivo nao foi encontrado:(")

    return token_lido