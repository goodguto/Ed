import ollama

MODELO_ESCOLHIDO = "deepseek-r1:8b"

def gerar_resposta_gm_ooc(mensagem_usuario):
    """
    Função para o comando ./GM. 
    A IA responde como um assistente técnico/mestre corrigindo o rumo.
    """
    instrucao = (
        "Você é o Assistente do Mestre de RPG (Co-GM). "
        "O jogador está apontando um erro, fazendo uma pergunta de regras ou ajustando a história.\n"
        "1. Seja breve e educado.\n"
        "2. Reconheça o erro ou a instrução.\n"
        "3. Confirme que entendeu para as próximas rodadas.\n"
        "4. NÃO narre a história aqui, apenas converse sobre ela."
    )
    
    try:
        resposta = ollama.chat(
            model=MODELO_ESCOLHIDO,
            messages=[
                {'role': 'system', 'content': instrucao},
                {'role': 'user', 'content': mensagem_usuario}
            ]
        )
        return resposta['message']['content']
    except Exception as e:
        return f"Erro de conexão OOC: {e}"

def gerar_resposta_rpg(nome_personagem, classe, atributos, historico_chat, mensagem_atual):
    instrucao_sistema = (
        "Você é o Mestre (GM) de uma aventura de RPG.\n"
        "--- DIRETRIZES ---\n"
        "1. IDIOMA: Português do Brasil.\n"
        "2. FORMATO: Apenas narre o resultado das ações. Não pergunte 'O que você faz?'.\n"
        "3. MEMÓRIA: Use o histórico para manter coerência (nomes, locais, inventário).\n"
        "4. ESTILO: Fantasia medieval, descritivo mas dinâmico.\n\n"
        f"--- PERSONAGEM ATUAL ---\n"
        f"Nome: {nome_personagem} | Classe: {classe}\n"
        f"Atributos: {atributos}"
    )

    mensagens_para_envio = [{'role': 'system', 'content': instrucao_sistema}]

    if historico_chat:
        for msg in historico_chat:
            role = "assistant" if msg['eh_bot'] else "user"
            mensagens_para_envio.append({
                'role': role,
                'content': msg['conteudo']
            })

    mensagens_para_envio.append({'role': 'user', 'content': mensagem_atual})

    try:
        resposta = ollama.chat(
            model=MODELO_ESCOLHIDO, 
            messages=mensagens_para_envio,
            options={'temperature': 0.7, 'num_ctx': 4096} 
        )
        texto = resposta['message']['content']
        
        if "</think>" in texto:
            texto = texto.split("</think>")[-1].strip()
            
        return texto
    except Exception as erro:
        print(f"Erro IA: {erro}")
        return "⚠️ O Mestre está meditando (Erro de conexão com o Ollama)."