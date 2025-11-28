import discord
from discord.ext import commands
from Bot.bot import carregar_token
intents = discord.Intents.all() #permissoes pro bot funcionar

bot = commands.Bot(command_prefix="./", intents=intents) #variavel para ter todas as propriedades do bot

token = carregar_token()

if token !="":
    bot.run(carregar_token)
else:
    print("token não foi encontrado. impossivel carregar o boss")
