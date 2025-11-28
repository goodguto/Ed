import discord
from discord.ext import commands
from Bot.bot import carregar_token
from Bot.dados import classes_rpg


intents = discord.Intents.all() #permissoes pro bot funcionar

bot = commands.Bot(command_prefix="./", intents=intents) #variavel para ter todas as propriedades do bot

token = carregar_token()

@bot.event
async def on_ready(): #função assincrona basica né
    print("Bot iniciado corretamente")

@bot.command()
async def saudacoes(ctx:commands.Context): #guarda informações (servidor, usuario, canal), que o comando foi chamado
    nome = ctx.author.display_name #pega o apelido no server
    await ctx.reply(f"Olá, {nome}! tudo certo?")

@bot.command()
async def comecar(ctx:commands.Context):
    nome = ctx.author.display_name
    mensagem = (
        f"Olá, {nome}! Bem-vindo ao seu novo RPG.\n"
        "Antes de continuarmos, peço que leia as instruções: ./instrucoes\n"
        "Caso já tenha lido, pode usar o comando: ./start"
    )
    await ctx.reply(mensagem)


@bot.command()    
async def instrucoes(ctx:commands.Context):
    embed_regras = discord.Embed(
        title="📜 Instruções e Regras da Mesa",
        description="Fico feliz por ter escolhido a mim para mestrar sua jornada! Aqui estão as diretrizes:",
        color=0x2ecc71
    )
    embed_regras.add_field(
        name="👥 Quantidade de Jogadores",
        value="Consigo mestrar para até 5 jogadores simultâneos. Mais que isso sobrecarrega meus circuitos mágicos.",
        inline=False
    )
    embed_regras.add_field(
        name="⚔️ Classes",
        value="Temos classes pré-estabelecidas. Digite `./classes` para ver a lista ou deixe que eu escolha baseada na sua personalidade.",
        inline=False
    )
    embed_regras.add_field(
        name="💀 Sistema de Morte",
        value="Morte não é o fim! Teste da Morte: role 3d20. Se passar na CD (Classe de Dificuldade), você vive.",
        inline=False
    )
    embed_regras.add_field(
        name="🚫 Boas Condutas (Zero Tolerância)",
        value="Chat reservado para o RPG ajuda na imersão.\n**IMPORTANTE:** Sem nazismo, fascismo ou discurso de ódio. O RPG será cancelado imediatamente se isso ocorrer.",
        inline=False
    )

    await ctx.send(embed=embed_regras)

#depois tenho que ajeitar. tá tudo muito colado
@bot.command()
async def classes(ctx: commands.Context):
    embed_classes = discord.Embed(
        title="⚔️ Classes Disponíveis",
        description="Atributos iniciais (Base 20). Escolha com sabedoria.",
        color=0xe74c3c
    )

    for nome_classe, atb in classes_rpg.items():
        texto_status = (
            f"{atb['icone']} **{atb['descricao']}**\n"
            f"💪 FOR: {atb['forca']} | 🤸 DES: {atb['destreza']} | ❤️ CON: {atb['constituição']}\n"
            f"🧠 INT: {atb['inteligencia']} | 🦉 SAB: {atb['sabedoria']} | 👄 CAR: {atb['carisma']}"
        )

        embed_classes.add_field(
            name=f"🔹 {nome_classe}",
            value=texto_status,
            inline=False
        )

    await ctx.send(embed=embed_classes)

if token !="":
    bot.run(token)
else:
    print("token não foi encontrado. impossivel carregar o boss")
