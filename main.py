import discord
import asyncio # Importante para não travar o bot
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

from Bot.ia import gerar_resposta_rpg, gerar_resposta_gm_ooc

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="./", intents=intents)
bot.remove_command('help')

token = carregar_token()

@bot.event
async def on_ready():
    print(f"Bot Online! Usando IA: DeepSeek-R1")

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
        value=(
            "`./instrucoes` - Regras do servidor.\n", 
            "`./tutorial` - Apagar um personagem."
        ),
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command()
async def saudacoes(ctx:commands.Context):
    nome = ctx.author.display_name
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

        await ctx.reply(f"Parabéns **{nome_personagem}**!! Agora você é um **{classe_formatada}**. Curta sua jornada com sabedoria")

    else:
        await ctx.reply(f"A classe que você escolheu não existe ainda :( . mas você pode dar uma olhada em ./classes para ver qual você mais gostou")

@bot.command()
async def meus_personagens(ctx:commands.Context):
    id_jogador = ctx.author.id
    lista = listar_personagens(id_jogador)

    if len(lista) > 0:
        texto_lista= ", ".join(lista)
        await ctx.reply(f"Seus personagens Slavos: **{texto_lista}**")
    else:
        await ctx.reply("Você não tem nenhum personagem")


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
        await ctx.reply("Você ainda não tem personagem. Use `./criar [Classe] [Nome]`")

@bot.command()
async def deletar(ctx:commands.Context, nome_personagem:str):
    id_jogador = ctx.author.id
    sucesso = deletar_personagem(id_jogador, nome_personagem)

    if sucesso: 
        await ctx.reply(f"O personagem **{nome_personagem}** foi deletado com sucesso")

    else:
        await ctx.reply(f"Você não tem um personagem **{nome_personagem}** para deletar")

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

@bot.command()
async def tutorial(ctx: commands.Context):
    embed = discord.Embed(
        title="📚 Como Jogar: Guia de Imersão",
        description="Para a melhor experiência possível, siga estas diretrizes:",
        color=0xf1c40f # Amarelo Dourado
    )
    
    embed.add_field(
        name="1. Canal Dedicado",
        value="Crie ou use um canal de texto APENAS para o RPG. Isso permite que eu leia o histórico e lembre do que aconteceu na história.",
        inline=False
    )
    
    embed.add_field(
        name="2. Comandos Básicos",
        value="Use `./acao [Sua Ação]` para jogar.\nExemplo: `./acao Olho em volta procurando armadilhas.`",
        inline=False
    )
    
    embed.add_field(
        name="3. Fichas",
        value="Mantenha sua ficha atualizada. Eu uso seus atributos para calcular se suas ações deram certo.",
        inline=False
    )

    await ctx.send(embed=embed)

@bot.command()
async def GM(ctx: commands.Context, *, mensagem: str):
    """
    Fala diretamente com a IA para corrigir erros ou tirar dúvidas.
    Ex: ./GM Você esqueceu que o taverneiro morreu.
    """
    async with ctx.typing():
        resposta = await asyncio.to_thread(gerar_resposta_gm_ooc, mensagem)
        await ctx.reply(f"🔧 **GM:** {resposta}")


@bot.command()
async def acao(ctx: commands.Context, *, mensagem_usuario: str):
    id_jogador = ctx.author.id
    
    # Carrega personagem 
    lista_chars = listar_personagens(id_jogador)
    if not lista_chars:
        await ctx.reply("Crie um personagem primeiro com `./criar`!")
        return
        
    nome_personagem = lista_chars[0]
    dados_ficha = carregar_personagem(id_jogador, nome_personagem)

    # Coleta o histórico 
    historico_formatado = []
    mensagens_anteriores = [msg async for msg in ctx.channel.history(limit=80)]
    mensagens_anteriores.reverse()

    for msg in mensagens_anteriores:
        if msg.id == ctx.message.id: continue 
        
        conteudo_limpo = msg.content
        eh_bot = (msg.author == bot.user)
        
        
        if not eh_bot:
            if msg.content.startswith("./acao "):
                conteudo_limpo = msg.content.replace("./acao ", "[JOGADOR]: ")
            elif msg.content.startswith("./GM "):
                conteudo_limpo = msg.content.replace("./GM ", "[OFF-GAME/Correção]: ")
            else:
                continue
        
        historico_formatado.append({
            "conteudo": conteudo_limpo,
            "eh_bot": eh_bot
        })

    async with ctx.typing():
        resposta_gm = await asyncio.to_thread(
            gerar_resposta_rpg,
            nome_personagem=dados_ficha['nome'],
            classe=dados_ficha['classe'],
            atributos=dados_ficha['atributos'],
            historico_chat=historico_formatado,
            mensagem_atual=f"[JOGADOR]: {mensagem_usuario}"
        )
        
        if len(resposta_gm) > 2000:
            pedacos = [resposta_gm[i:i+1900] for i in range(0, len(resposta_gm), 1900)]
            for pedaco in pedacos:
                await ctx.reply(pedaco)
        else:
            await ctx.reply(resposta_gm)

if token != "":
    bot.run(token)
else:
    print("token não foi encontrado. impossivel carregar o boss")