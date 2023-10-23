import pygame
import random
import time

# Inicialização do Pygame
pygame.init()

# Configurações da tela
tela_largura = 1200
tela_altura = 900
branco = (255, 255, 255)
preto = (0, 0, 0)
tela = pygame.display.set_mode((tela_largura, tela_altura))
pygame.display.set_caption("Survive Nature")

# Carregando imagens
cenario1 = pygame.image.load("cenario1.png")
cenario2 = pygame.image.load("cenario2.png")
cenario3 = pygame.image.load("cenario3.png")
cenario4 = pygame.image.load("cenario4.png")
vila_fundo = pygame.image.load("vilafundo.png")
prefeitura = pygame.image.load("prefeitura1.png")
jogador = pygame.image.load("jogador.png")
arvore = pygame.image.load("arvore.png")
pedra_img = pygame.image.load("pedra.png")
ferro_img = pygame.image.load("ferro.png")

# Posição inicial do jogador
jogador_x = 400
jogador_y = 500

# Limites da tela do jogo
limite_esquerda_tela = 0
limite_direita_tela = tela_largura
limite_superior_tela = 0
limite_inferior_tela = tela_altura

# Limites do jogador dentro do cenário
limite_esquerda_cenario = 0
limite_direita_cenario = cenario1.get_width() - jogador.get_width()

# Variáveis de recursos
recursos = {
    "madeira": 100,
    "pedra": 100,
    "ferro": 100,
}

# Fonte para exibir informações na tela
fonte = pygame.font.Font(None, 36)

# Velocidade do jogador
velocidade = 5

# Variáveis para controle de árvores, pedras e ferro
arvores = []
pedras = []
ferro = []

# Variável para controlar se o jogador está na vila
na_vila = False

# Função para alternar entre a tela da vila e o jogo principal
def alternar_vila():
    global na_vila
    na_vila = not na_vila

def posicao_segura(nova_x, nova_y, construcoes, distancia_minima, distancia_minima_entre_construcoes):
    for x, y in construcoes:
        if abs(nova_x - x) < distancia_minima_entre_construcoes and abs(nova_y - y) < distancia_minima_entre_construcoes:
            return False
    return True

def gerar_arvores(distancia_minima, distancia_minima_entre_construcoes):
    numero_arvores = 2
    arvores.clear()
    for _ in range(numero_arvores):
        while True:
            x = random.randint(limite_esquerda_cenario, limite_direita_cenario)
            y = random.randint(tela_altura // 2, tela_altura - arvore.get_height())
            if posicao_segura(x, y, arvores, distancia_minima, distancia_minima_entre_construcoes):
                arvores.append((x, y))
                break

def gerar_pedras(distancia_minima, distancia_minima_entre_construcoes):
    numero_pedras = 1
    pedras.clear()
    for _ in range(numero_pedras):
        while True:
            x = random.randint(limite_esquerda_cenario, limite_direita_cenario)
            y = random.randint(tela_altura // 2, tela_altura - pedra_img.get_height())
            if posicao_segura(x, y, pedras, distancia_minima, distancia_minima_entre_construcoes):
                pedras.append((x, y))
                break

def gerar_ferro(distancia_minima, distancia_minima_entre_construcoes):
    numero_ferro = 1
    ferro.clear()
    for _ in range(numero_ferro):
        while True:
            x = random.randint(limite_esquerda_cenario, limite_direita_cenario)
            y = random.randint(tela_altura // 2, tela_altura - ferro_img.get_height())
            if posicao_segura(x, y, ferro, distancia_minima, distancia_minima_entre_construcoes):
                ferro.append((x, y))
                break


prefeitura_x = 100  # Defina a posição X da prefeitura
prefeitura_y = 500  # Defina a posição Y da prefeitura
nome_construcao = "Prefeitura"
construcoes = {
    "Prefeitura": {"nivel": 1, "madeira": 0, "pedra": 0, "ferro": 0},
}

# Variáveis para controlar a interface de construções
construcoes_aberto = False
construcao_selecionada = None

aba_selecionada = "Para Evoluir"

def desenhar_interface_construcoes():
    tela_construcoes = pygame.Surface((tela_largura, tela_altura))
    tela_construcoes.fill((200, 200, 200))

    # Desenha a interface de recursos
    # (Adicione aqui o código para desenhar sua interface de recursos)

    # Desenha as abas
    abas = ["Para Evoluir", "Para Construir", "Suas Construções e Níveis"]
    largura_aba = 200
    altura_aba = 40
    espacamento_abas = 10

    for i, aba in enumerate(abas):
        x_aba = 10 + (largura_aba + espacamento_abas) * i
        y_aba = 400  # Ajuste a posição vertical aqui
        pygame.draw.rect(tela_construcoes, (255, 255, 255), (x_aba, y_aba, largura_aba, altura_aba))
        texto_aba = fonte.render(aba, True, (0, 0, 0))
        tela_construcoes.blit(texto_aba, (x_aba + 10, y_aba + 10))

        if aba == aba_selecionada:
            pygame.draw.rect(tela_construcoes, (0, 255, 0), (x_aba, y_aba, largura_aba, altura_aba))

    if aba_selecionada == "Para Evoluir":
        if "Prefeitura" in construcoes:
            nivel_prefeitura = construcoes["Prefeitura"]["nivel"]
            if nivel_prefeitura < 3:
                custo_madeira = 0
                custo_pedra = 0
                custo_ferro = 0

                if nivel_prefeitura == 1:
                    custo_madeira = 20
                    custo_pedra = 10
                elif nivel_prefeitura == 2:
                    custo_madeira = 30
                    custo_pedra = 20
                    custo_ferro = 10

                pygame.draw.rect(tela_construcoes, (255, 0, 0), (10, 450, 370, 50))
                texto_construcao = fonte.render(f"Prefeitura (Nível {nivel_prefeitura + 1})", True, (0, 0, 0))
                tela_construcoes.blit(texto_construcao, (20, 450))

                # Exibe os recursos necessários
                texto_recursos = fonte.render(f"Recursos necessários: Madeira {custo_madeira}, Pedra {custo_pedra}, Ferro {custo_ferro}", True, (0, 0, 0))
                tela_construcoes.blit(texto_recursos, (20, 500))

                if recursos["madeira"] >= custo_madeira and recursos["pedra"] >= custo_pedra and recursos["ferro"] >= custo_ferro:
                    pygame.draw.rect(tela_construcoes, (0, 255, 0), (300, 450, 80, 40))
                    texto_evolver = fonte.render("Evoluir", True, (0, 0, 0))
                    tela_construcoes.blit(texto_evolver, (310, 460))
                else:
                    pygame.draw.rect(tela_construcoes, (255, 0, 0), (10, 450, 370, 50))
                    texto_construcao = fonte.render(f"Recursos insuficientes", True, (0, 0, 0))
                    tela_construcoes.blit(texto_construcao, (20, 450))

    elif aba_selecionada == "Suas Construções e Níveis":
        # Conteúdo da aba "Suas Construções e Níveis"
        for construcao, info in construcoes.items():
            texto_construcao = fonte.render(f"{construcao} (Nível {info['nivel']})", True, (0, 0, 0))
            tela_construcoes.blit(texto_construcao, (10, 450))

    if aviso:
        pygame.draw.rect(tela_construcoes, (255, 0, 0), (10, tela_altura - 100, tela_largura - 20, 40))
        texto_aviso = fonte.render(aviso, True, (255, 255, 255))
        tela_construcoes.blit(texto_aviso, (20, tela_altura - 90))

    if construcao_selecionada:
        pygame.draw.rect(tela_construcoes, (0, 255, 0), (tela_largura - 250, tela_altura - 60, 240, 40))
        texto_construir = fonte.render("Construir", True, (0, 0, 0))
        tela_construcoes.blit(texto_construir, (tela_largura - 240, tela_altura - 50))

    tela.blit(tela_construcoes, (0, 0))

def evoluir_construcao(construcoes, recursos, aba_selecionada):
    if aba_selecionada == "Para Evoluir":
        if "Prefeitura" in construcoes:
            nivel_prefeitura = construcoes["Prefeitura"]["nivel"]
            if nivel_prefeitura < 3:
                custo_madeira = 0
                custo_pedra = 0
                custo_ferro = 0

                if nivel_prefeitura == 1:
                    custo_madeira = 20
                    custo_pedra = 10
                elif nivel_prefeitura == 2:
                    custo_madeira = 30
                    custo_pedra = 20
                    custo_ferro = 10

                if recursos["madeira"] >= custo_madeira and recursos["pedra"] >= custo_pedra and recursos["ferro"] >= custo_ferro:
                    # Realiza a evolução da construção aqui
                    # Por exemplo, você pode aumentar o nível da Prefeitura e deduzir os recursos necessários
                    construcoes["Prefeitura"]["nivel"] += 1
                    recursos["madeira"] -= custo_madeira
                    recursos["pedra"] -= custo_pedra
                    recursos["ferro"] -= custo_ferro



# Altere a função para comprar construções
def comprar_construcao(construcao):
    global aviso
    global recursos

    if construcao in construcoes:
        custo = construcoes[construcao]
        if all(recursos[recurso] >= custo[recurso] for recurso in custo):
            for recurso in custo:
                recursos[recurso] -= custo[recurso]
            aviso = f"{construcao} construída!"
        else:
            aviso = "Recursos insuficientes para construir a construção."
    else:
        aviso = "Construção não encontrada."

# Adicione a funcionalidade de clique para a interface de construções
    if evento.type == pygame.MOUSEBUTTONDOWN:
        if evento.button == 1:  # Botão esquerdo do mouse
            if construcoes_aberto:
                if tela_largura - 400 <= evento.pos[0] <= tela_largura and 0 <= evento.pos[1] <= tela_altura:
                    comprar_construcao("Prefeitura")
                elif construcao_selecionada and tela_largura - 250 <= evento.pos[0] <= tela_largura and tela_altura - 60 <= evento.pos[1] <= tela_altura:
                    evoluir_construcao(construcao_selecionada)

# Altere a função para desenhar a tela da vila
def desenhar_vila():
    tela.blit(vila_fundo, (0, 0))
    tela.blit(prefeitura, (prefeitura_x, prefeitura_y))
    desenhar_botao_principal()
    desenhar_botao_construcoes()  # Adicione esta linha para desenhar o botão "Construções"
    desenhar_interface_recursos()

    # Exibir o nome da construção abaixo da imagem
    nome_construcao = "Prefeitura"
    texto_construcao = fonte.render(nome_construcao, True, (0, 0, 0))
    largura_texto, altura_texto = fonte.size(nome_construcao)
    x_texto = prefeitura_x + (prefeitura.get_width() - largura_texto) // 2
    y_texto = prefeitura_y + prefeitura.get_height() + 5  # Distância reduzida
    tela.blit(texto_construcao, (x_texto, y_texto))

# Adicione botões na tela
botao_vila_x = tela_largura - 100
botao_vila_y = 60
botao_vila_largura = 90
botao_vila_altura = 40

botao_principal_x = tela_largura - 150
botao_principal_y = 10
botao_principal_largura = 130
botao_principal_altura = 50

# Adicione o botão "Construções" na tela da vila
botao_construcoes_x = tela_largura - 200
botao_construcoes_y = botao_vila_y + botao_vila_altura # Aumente a distância em 10 pixels
botao_construcoes_largura = 180
botao_construcoes_altura = 40

# Função para desenhar o botão "Construções"
def desenhar_botao_construcoes():
    pygame.draw.rect(tela, (0, 0, 255), (botao_construcoes_x, botao_construcoes_y, botao_construcoes_largura, botao_construcoes_altura))
    texto_construcoes = fonte.render("Construções", True, (255, 255, 255))
    tela.blit(texto_construcoes, (botao_construcoes_x + 10, botao_construcoes_y + 10))

def desenhar_botao_vila():
    pygame.draw.rect(tela, (0, 0, 255), (botao_vila_x, botao_vila_y, botao_vila_largura, botao_vila_altura))
    texto_vila = fonte.render("Vila", True, (255, 255, 255))
    tela.blit(texto_vila, (botao_vila_x + 10, botao_vila_y + 10))

def desenhar_botao_principal():
    pygame.draw.rect(tela, (0, 0, 255), (botao_principal_x, botao_principal_y, botao_principal_largura, botao_principal_altura))
    texto_principal = fonte.render("Aventura", True, (255, 255, 255))
    tela.blit(texto_principal, (botao_principal_x + 10, botao_principal_y + 10))


# Variável para o aviso
aviso = ""
aviso_duracao = 3
tempo_do_aviso = 0

# Variáveis para crafting
itens_craft = {
    "Picareta de Madeira": {"madeira": 5},
    "Picareta de Pedra": {"pedra": 10},
    "Picareta de Ferro": {"ferro": 10},
}

itens_disponíveis = {
    "Picareta de Madeira": {"madeira": 5},
    "Picareta de Pedra": {"pedra": 10},
    "Picareta de Ferro": {"ferro": 10},
}

itens_comprados = {}
possui_picareta_de_pedra = False  # Variável para verificar se o jogador possui a picareta de pedra
possui_picareta_de_ferro = False  # Variável para verificar se o jogador possui a picareta de ferro
item_selecionado = None
craft_aberto = False

# Posição do botão de craft
botão_craft_x = tela_largura - 100
botão_craft_y = 10
botão_craft_largura = 90
botão_craft_altura = 40

def desenhar_cenario(cenario):
    tela.blit(cenario, (0, 0))
    for x, y in pedras:
        tela.blit(pedra_img, (x, y))  # Desenhar pedras antes do jogador e das árvores
    for x, y in arvores:
        tela.blit(arvore, (x, y))
    for x, y in ferro:
        tela.blit(ferro_img, (x, y))  # Desenhar minério de ferro
    tela.blit(jogador, (jogador_x, jogador_y))

    # Exibir informações na tela
    for i, (recurso, quantidade) in enumerate(recursos.items()):
        texto_recurso = fonte.render(f"{recurso.capitalize()}: {quantidade}", True, (255, 255, 255))
        tela.blit(texto_recurso, (10, 10 + i * 40))

    pygame.display.update()

def desenhar_botão_craft():
    pygame.draw.rect(tela, (0, 255, 0), (botão_craft_x, botão_craft_y, botão_craft_largura, botão_craft_altura))
    texto_craft = fonte.render("Craft", True, (0, 0, 0))
    tela.blit(texto_craft, (botão_craft_x + 10, botão_craft_y + 10))

def abrir_fechar_craft():
    global craft_aberto
    craft_aberto = not craft_aberto

def desenhar_interface_craft():
    tela_craft = pygame.Surface((tela_largura, tela_altura))
    tela_craft.fill((200, 200, 200))

    for i, (recurso, quantidade) in enumerate(recursos.items()):
        texto_recurso = fonte.render(f"{recurso.capitalize()}: {quantidade}", True, (0, 0, 0))
        tela_craft.blit(texto_recurso, (10, 10 + i * 40))

    if not item_selecionado:
        texto_selecione = fonte.render("Selecione um item para craft", True, (0, 0, 0))
        tela_craft.blit(texto_selecione, (tela_largura - 380, 10))

    for i, (item, ingredientes) in enumerate(itens_disponíveis.items()):
        pygame.draw.rect(tela_craft, (255, 255, 255), (tela_largura - 380, 60 + i * 60, 370, 50))
        texto_item = fonte.render(f"{item}", True, (0, 0, 0))
        tela_craft.blit(texto_item, (tela_largura - 370, 60 + i * 60))
        texto_ingredientes = fonte.render(f"{', '.join([f'{q} {i}' for i, q in ingredientes.items()])}", True, (0, 0, 0))
        tela_craft.blit(texto_ingredientes, (tela_largura - 370, 90 + i * 60))

    for i, (item, ingredientes) in enumerate(itens_comprados.items()):
        espacamento_vertical = 60
        pygame.draw.rect(tela_craft, (200, 200, 200), (10, 200 + i * espacamento_vertical, 370, 50))
        texto_item = fonte.render(f"{item}", True, (0, 0, 0))
        tela_craft.blit(texto_item, (20, 200 + i * espacamento_vertical))
        texto_ingredientes = fonte.render(f"{', '.join([f'{q} {i}' for i, q in ingredientes.items()])}", True, (0, 0, 0))
        tela_craft.blit(texto_ingredientes, (20, 230 + i * espacamento_vertical))

    if item_selecionado:
        pygame.draw.rect(tela_craft, (0, 255, 0), (tela_largura - 250, tela_altura - 60, 240, 40))
        texto_craft = fonte.render("Craft", True, (0, 0, 0))
        tela_craft.blit(texto_craft, (tela_largura - 240, tela_altura - 50))

    if aviso:
        pygame.draw.rect(tela_craft, (255, 0, 0), (10, tela_altura - 100, tela_largura - 20, 40))
        texto_aviso = fonte.render(aviso, True, (255, 255, 255))
        tela_craft.blit(texto_aviso, (20, tela_altura - 90))

    tela.blit(tela_craft, (0, 0))

def comprar_item(item):
    global item_selecionado
    global recursos
    global aviso
    global possui_picareta_de_pedra
    global possui_picareta_de_ferro

    ingredientes = itens_disponíveis.get(item, None)

    if ingredientes:
        recursos_suficientes = True
        for recurso, quantidade in ingredientes.items():
            if recursos.get(recurso, 0) < quantidade:
                recursos_suficientes = False
                break

        if recursos_suficientes:
            item_selecionado = item
            for recurso, quantidade in ingredientes.items():
                recursos[recurso] -= quantidade
            if item in itens_disponíveis:
                itens_disponíveis.pop(item)
                itens_comprados[item] = ingredientes
                aviso = f"Você comprou {item}, parabéns!"
                if item == "Picareta de Ferro":
                    possui_picareta_de_ferro = True  # Define que o jogador possui a picareta de ferro
        else:
            aviso = "Você não possui recursos suficientes"

def coletar_madeira():
    for i, (x, y) in enumerate(arvores):
        if jogador_x <= x <= jogador_x + jogador.get_width() and jogador_y <= y + arvore.get_height():
            arvores.pop(i)
            recursos["madeira"] += 1
            if possui_picareta_de_ferro:
                recursos["madeira"] += 1  # Duplica a madeira quando o jogador tem a picareta de ferro

def coletar_pedra():
    global aviso, tempo_do_aviso, possui_picareta_de_pedra

    if possui_picareta_de_pedra:
        for i, (x, y) in enumerate(pedras):
            if jogador_x <= x <= jogador_x + jogador.get_width() and jogador_y <= y + pedra_img.get_height():
                pedras.pop(i)
                recursos["pedra"] += 1
                if possui_picareta_de_ferro:
                    recursos["pedra"] += 1  # Duplica a pedra quando o jogador tem a picareta de ferro
    else:
        aviso = "Você precisa da picareta de pedra para coletar pedra."
        tempo_do_aviso = time.time()

def coletar_ferro():
    global aviso, tempo_do_aviso, possui_picareta_de_pedra

    if "Picareta de Pedra" in itens_comprados:  # Verifica se o jogador possui a picareta de pedra
        for i, (x, y) in enumerate(ferro):
            if jogador_x <= x <= jogador_x + jogador.get_width() and jogador_y <= y + ferro_img.get_height():
                ferro.pop(i)
                recursos["ferro"] += 1
                if possui_picareta_de_ferro:
                    recursos["ferro"] += 1  # Duplica o ferro quando o jogador tem a picareta de ferro
    else:
        aviso = "Você precisa da picareta de pedra para coletar ferro."
        tempo_do_aviso = time.time()

def desenhar_interface_recursos():
    for i, (recurso, quantidade) in enumerate(recursos.items()):
        texto_recurso = fonte.render(f"{recurso.capitalize()}: {quantidade}", True, (255, 255, 255))
        tela.blit(texto_recurso, (10, 10 + i * 40))

# Inicialmente, mostramos o primeiro cenário
cenario_atual = cenario1
gerar_arvores(50, 100)
gerar_pedras(100, 100)
gerar_ferro(200, 100)

# Loop principal
executando = True
while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:
                abrir_fechar_craft()
            elif evento.key == pygame.K_t:
                alternar_vila()
            elif evento.key == pygame.K_c:  # Adicione o atalho para abrir/fechar a interface de construções
                construcoes_aberto = not construcoes_aberto

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:  # Botão esquerdo do mouse
                if not craft_aberto:
                    coletar_madeira()
                    coletar_pedra()
                    coletar_ferro()
                else:
                    if tela_largura - 400 <= evento.pos[0] <= tela_largura and 0 <= evento.pos[1] <= tela_altura:
                        comprar_item("Picareta de Madeira")
                        comprar_item("Picareta de Pedra")
                        comprar_item("Picareta de Ferro")
                        if "Picareta de Madeira" in itens_comprados or "Picareta de Pedra" in itens_comprados:
                            possui_picareta_de_pedra = True

                # Verifique se o jogador clicou no botão de construções
                if botao_construcoes_x <= evento.pos[0] <= botao_construcoes_x + botao_construcoes_largura and \
                        botao_construcoes_y <= evento.pos[1] <= botao_construcoes_y + botao_construcoes_altura:
                        construcoes_aberto = not construcoes_aberto
                
                if evento.button == 1:  # Verifica se o botão esquerdo do mouse foi clicado
                    x, y = evento.pos  # Obtém as coordenadas do clique

            # Verifique se um clique ocorreu nas abas
                if y >= 400 and y <= 440:
                    if x >= 10 and x <= 210:
                        aba_selecionada = "Para Evoluir"
                    elif x >= 220 and x <= 420:
                        aba_selecionada = "Para Construir"
                    elif x >= 430 and x <= 630:
                        aba_selecionada = "Suas Construções e Níveis"
                    evoluir_construcao(construcoes, recursos, aba_selecionada)
                                
                # Verifique se o jogador clicou nos botões de "Vila" ou "Principal"
                if not craft_aberto:
                    if na_vila:
                        if botao_principal_x <= evento.pos[0] <= botao_principal_x + botao_principal_largura and \
                                botao_principal_y <= evento.pos[1] <= botao_principal_y + botao_principal_altura:
                            alternar_vila()
                    else:
                        if botao_vila_x <= evento.pos[0] <= botao_vila_x + botao_vila_largura and \
                                botao_vila_y <= evento.pos[1] <= botao_vila_y + botao_vila_altura:
                            alternar_vila()


    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_a] and jogador_x > limite_esquerda_cenario:
        jogador_x -= velocidade
    if teclas[pygame.K_d] and jogador_x < limite_direita_cenario:
        jogador_x += velocidade

    if jogador_x <= limite_esquerda_cenario:
        if cenario_atual == cenario1:
            cenario_atual = cenario2
            jogador_x = limite_direita_cenario
        elif cenario_atual == cenario2:
            cenario_atual = cenario1
            jogador_x = limite_direita_cenario
        elif cenario_atual == cenario3:
            cenario_atual = cenario2
            jogador_x = limite_direita_cenario
        elif cenario_atual == cenario4:
            cenario_atual = cenario3
            jogador_x = limite_direita_cenario
        gerar_arvores(50, 100)
        gerar_pedras(100, 100)
        gerar_ferro(200, 100)

    elif jogador_x >= limite_direita_cenario:
        if cenario_atual == cenario1:
            cenario_atual = cenario2
            jogador_x = limite_esquerda_cenario
        elif cenario_atual == cenario2:
            cenario_atual = cenario1
            jogador_x = limite_esquerda_cenario
        elif cenario_atual == cenario3:
            cenario_atual = cenario4
            jogador_x = limite_esquerda_cenario
        elif cenario_atual == cenario4:
            cenario_atual = cenario3
            jogador_x = limite_esquerda_cenario
        gerar_arvores(50, 100)
        gerar_pedras(100, 100)
        gerar_ferro(200, 100)

    
     # Desenhar construções na aba "Para Evoluir"
    if aba_selecionada == "Para Evoluir":
        for construcao, info in construcoes.items():
            if info['nivel'] < 3:
                texto_construcao = fonte.render(f"{construcao} (Nível {info['nivel']})", True, preto)
                tela.blit(texto_construcao, (20, 100))

    # Desenhar informações de recursos
    texto_recursos = fonte.render(f"Recursos: Madeira {recursos['madeira']} Pedra {recursos['pedra']} Ferro {recursos['ferro']}", True, preto)
    tela.blit(texto_recursos, (20, 20))

    # Desenhar aviso
    texto_aviso = fonte.render(aviso, True, (255, 0, 0))
    tela.blit(texto_aviso, (20, 550))

    if not craft_aberto:
        if na_vila:
            desenhar_vila()
            if construcoes_aberto:
                desenhar_interface_construcoes()
        else:
            desenhar_cenario(cenario_atual)
            desenhar_botao_vila()
            desenhar_botão_craft()
        desenhar_interface_recursos()
    else:
        desenhar_interface_craft()

    if aviso and time.time() - tempo_do_aviso >= aviso_duracao:
        aviso = ""

    pygame.display.update()

# Finaliza o jogo
pygame.quit()