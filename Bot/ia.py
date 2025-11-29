import ollama

MODELO_ESCOLHIDO = "llama3"

def gerar_resposta_rpg(nome_personagem, classe, atributos, historico_chat, mensagem_usuario):
    
    #melhorar o prompt
    instrucao_sistema = (
        "Você é um Mestre de RPG (Game Master/GM) experiente, criativo e justo. "
        "Você está mestrando uma aventura de fantasia medieval.\n"
        "Regras:\n"
        "1. Responda em português do Brasil.\n"
        "2. Seja descritivo, mas não escreva textos longos demais (máximo 3 parágrafos).\n"
        "3. Se o jogador tentar algo impossível, descreva a falha ou peça um teste de dados.\n"
        "4. Controle os NPCs e o ambiente.\n"
        "5. NUNCA decida as ações do jogador, apenas reaja a elas.\n\n"
        f"Dados do Jogador Atual:\n"
        f"Nome: {nome_personagem} | Classe: {classe}\n"
        f"Atributos: {atributos}"
    )

    mensagens_para_envio = []
    
    mensagens_para_envio.append({
        'role': 'system',
        'content': instrucao_sistema
    })


    mensagens_para_envio.append({
        'role': 'user',
        'content': mensagem_usuario
    })

    print(" IA Pensando...") # log
    
    try:
        # chamada pra ollama local
        resposta = ollama.chat(model=MODELO_ESCOLHIDO, messages=mensagens_para_envio)
        
        texto_resposta = resposta['message']['content']
        return texto_resposta
        
    except Exception as erro:
        print(f"Erro na IA: {erro}")
        return "O Mestre está confuso (Erro de conexão com o Ollama local)."