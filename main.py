import discord
from discord.ext import commands
from Bot.bot import carregar_token
from Bot.dados import classes_rpg
from Bot.jogadores import (
    salvar_personagem, 
    carregar_personagem, 
    deletar_personagem,
    personagem_existe, 
    listar_personagens,
    renomear_personagem, 
    editar_atributo_personagem
)

intents = discord.Intents.all() #permissoes pro bot funcionar

bot = commands.Bot(command_prefix="./", intents=intents) #variavel para ter todas as propriedades do bot

token = carregar_token()

@bot.event
async def on_ready(): 
    print("Bot iniciado corretamente")
@bot.command()
async def menu(ctx: commands.Context):
    embed = discord.Embed(
        title="📜 Menu de Comandos do RPG",
        description="Guia rápido para sua aventura.",
        color=0x3498db
    )
    
    embed.add_field(
        name="🐣 Criação e Personagens", 
        value=(
            "`./classes` - Ver classes disponíveis.\n"
            "`./criar [Classe] [Nome]` - Criar novo personagem.\n"
            "`./meus_personagens` - Listar seus heróis.\n"
            "`./perfil [Nome]` - Ver a ficha completa."
        ), 
        inline=False
    )
    
    embed.add_field(
        name="⚙️ Gerenciamento", 
        value=(
            "`./renomear [NomeAntigo] [NomeNovo]` - Mudar nome do personagem.\n"
            "`./editar [Nome] [Atributo] [Valor]` - Alterar status (Ex: forca 15).\n"
            "`./deletar [Nome]` - Apagar um personagem."
        ), 
        inline=False
    )
    
    embed.add_field(
        name="❓ Outros", 
        value="`./instrucoes` - Regras do servidor.", 
        inline=False
    )
    
    await ctx.send(embed=embed)

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


#proximo passo é fazer a função aceitar nome composto. na realidade isso até é fácil. mas n é o foco agora
@bot.command()
async def criar(ctx:commands.Context, nome_classe: str, nome_personagem:str):
    id_jogador = ctx.author.id
    nome_jogador = ctx.author.display_name
    classe_formatada = nome_classe.capitalize().strip()

    if personagem_existe(id_jogador, nome_personagem):
        await ctx.reply(f"Você já possui um personagem com o nome **{nome_personagem}**. Vamos manter a originalidade kkkkkkk, tenta outro")
        return
        
    
    if classe_formatada in classes_rpg:
        atributos_base = classes_rpg[classe_formatada]

        nova_ficha={
            "nome": nome_personagem,
            "dono_id": id_jogador,
            "classe": classe_formatada,
            "nivel": 1,
            "xp": 0,
            "pontos_livres": 0,
            "atributos": atributos_base,
            "dinheiro": 0,
            "inventario": None,
        }

        salvar_personagem(id_jogador,nome_personagem, nova_ficha)

        await ctx.reply(f"Parabéns **{nome_personagem}**!! Agora você é um **{classe_formatada}**. Curta sua jornado com sabedoria")

    else:
        await ctx.reply(f"a classe que você escolheu não existe ainda :( . mas você pode dar uma olhada em ./classes para ver qual você mais gostou")
@bot.command()
async def meus_personagens(ctx:commands.Context):
    id_jogador = ctx.author.id
    lista = listar_personagens(id_jogador)

    if len(lista) > 0:
        texto_lista= ", ".join(lista)
        await ctx.reply(f"Seus personagens Slavos: **{texto_lista}**")
    else:
        await ctx.reply("você não tem nenhum personagem")


@bot.command()
async def perfil(ctx:commands.Context, nome_personagem:str):
    id_jogador = ctx.author.id
    dados = carregar_personagem(id_jogador, nome_personagem)

    if dados:
        atb = dados["atributos"]
        texto_perfil = (
            f"👤 **Personagem:** {dados['nome']}\n"
            f"🛡️ **Classe:** {dados['classe']} (Nível {dados['nivel']})\n\n"
            f"**Atributos:**\n"
            f"💪 Força: {atb['forca']}\n"
            f"🤸 Destreza: {atb['destreza']}\n"
            f"❤️ Constituição: {atb['constituicao']}\n" 
            f"🧠 Inteligência: {atb['inteligencia']}\n"
            f"🦉 Sabedoria: {atb['sabedoria']}\n"
            f"👄 Carisma: {atb['carisma']}"
        )
        
        await ctx.reply(texto_perfil)
    else:
        await ctx.reply("Você ainda não tem personagem. Use ./escolher_classe + o nome da classe que voce quer")

# @bot.command()
# async def editar(ctx:commands.Context, novo_nome:str):
#     id_jogador = ctx.author.id
#     dados = carregar_personagem(id_jogador)

#     if dados:
#         dados["nomes"]: novo_nome
#         salvar_personagem(id_jogador, dados)
#         await ctx.reply(f"Nome editado para **{novo_nome}**!")
#     else:
#         await ctx.reply(f"Crie um personagem antes de tentar editalo")

@bot.command()
async def deletar(ctx:commands.Context, nome_personagem:str):
    id_jogador = ctx.author.id
    sucesso = deletar_personagem(id_jogador, nome_personagem)

    if sucesso: 
        await ctx.reply(f"O personagem**{nome_personagem}** foi deletado com sucesso")

    else:
        await ctx.reply(f"você não tem um personagem "**{nome_personagem}**" para deletar")

@bot.command()
async def renomear(ctx: commands.Context, nome_antigo: str, nome_novo: str):
    id_jogador = ctx.author.id
    
    
    sucesso, mensagem = renomear_personagem(id_jogador, nome_antigo, nome_novo)
    
    if sucesso:
        await ctx.reply(f"✅ Personagem renomeado de **{nome_antigo}** para **{nome_novo}**!")
    else:
        await ctx.reply(f"❌ Erro: {mensagem}")


@bot.command()
async def editar(ctx: commands.Context, nome_char: str, atributo: str, valor: int):
    id_jogador = ctx.author.id
    
    
    sucesso, mensagem = editar_atributo_personagem(id_jogador, nome_char, atributo, valor)
    
    if sucesso:
        await ctx.reply(f"✅ Atualização: {mensagem}")
    else:
        await ctx.reply(f"❌ Erro: {mensagem}")

if token !="":
    bot.run(token)
else:
    print("token não foi encontrado. impossivel carregar o boss")
