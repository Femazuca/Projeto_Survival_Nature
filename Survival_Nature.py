import pygame
import random
import time

# Inicialização do Pygame
pygame.init()

# Configurações da tela
tela_largura = 1200
tela_altura = 900
tela = pygame.display.set_mode((tela_largura, tela_altura))
pygame.display.set_caption("Survive Nature")

# Carregando imagens
cenario1 = pygame.image.load("cenario1.png")
cenario2 = pygame.image.load("cenario2.png")
cenario3 = pygame.image.load("cenario3.png")
cenario4 = pygame.image.load("cenario4.png")
jogador = pygame.image.load("jogador.png")
arvore = pygame.image.load("arvore.png")
pedra_img = pygame.image.load("pedra.png")
ferro_img = pygame.image.load("ferro.png")
nivel1_img = pygame.image.load("Nivel1.png")

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
            x = random.randint(limite_esquerda_cenario, limite_direita_cenario - arvore.get_width())
            y = random.randint(tela_altura // 2, tela_altura - arvore.get_height())
            if posicao_segura(x, y, arvores, distancia_minima, distancia_minima_entre_construcoes):
                arvores.append((x, y))
                break

def gerar_pedras(distancia_minima, distancia_minima_entre_construcoes):
    numero_pedras = 1
    pedras.clear()
    for _ in range(numero_pedras):
        while True:
            x = random.randint(limite_esquerda_cenario, limite_direita_cenario - pedra_img.get_width())
            y = random.randint(tela_altura // 2, tela_altura - pedra_img.get_height())
            if posicao_segura(x, y, pedras, distancia_minima, distancia_minima_entre_construcoes):
                pedras.append((x, y))
                break

def gerar_ferro(distancia_minima, distancia_minima_entre_construcoes):
    numero_ferro = 1
    ferro.clear()
    for _ in range(numero_ferro):
        while True:
            x = random.randint(limite_esquerda_cenario, limite_direita_cenario - ferro_img.get_width())
            y = random.randint(tela_altura // 2, tela_altura - ferro_img.get_height())
            if posicao_segura(x, y, ferro, distancia_minima, distancia_minima_entre_construcoes):
                ferro.append((x, y))
                break

# Variável para o aviso
aviso = ""
aviso_duracao = 3
tempo_do_aviso = 0

# Variáveis para crafting
itens_craft = {
    "Picareta de Madeira": {"madeira": 5},
    "Picareta de Pedra": {"pedra": 10},
    "Picareta de Ferro": {"ferro": 10},
    "Prefeitura": {"madeira": 20, "pedra": 20},
    "Muro": {"madeira": 40, "pedra": 30, "ferro": 10},
    "Bunker": {"ferro": 40}
}

itens_disponíveis = {
    "Picareta de Madeira": {"madeira": 5},
    "Picareta de Pedra": {"pedra": 10},
    "Picareta de Ferro": {"ferro": 10},
    "Prefeitura": {"madeira": 20, "pedra": 20},
    "Muro": {"madeira": 40, "pedra": 30, "ferro": 10},
    "Bunker": {"ferro": 40},
}

itens_comprados = {}
possui_picareta_de_pedra = False  # Variável para verificar se o jogador possui a picareta de pedra
possui_picareta_de_ferro = False  # Variável para verificar se o jogador possui a picareta de ferro
item_selecionado = None
craft_aberto = False
prefeitura_comprada = False
imagem_aberta = False

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
    global item_selecionado, recursos, aviso, possui_picareta_de_pedra, imagem_aberta, nivel1_surface

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
                if item == "Prefeitura":
                    imagem_aberta = True  # A imagem é exibida após a compra da prefeitura
                    nivel1_surface = nivel1_img  # Carregue a imagem Nível 1
                aviso = f"Você comprou {item}, parabéns!"
                if item == "Picareta de Ferro":
                    possui_picareta_de_ferro = True  

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

imagem_aberta = False
nivel1_surface = None

def desenhar_nivel():
    global nivel1_surface, imagem_aberta

    if "Prefeitura" in itens_comprados:
        if nivel1_surface is not None and imagem_aberta:
            tela.blit(nivel1_surface, ((tela_largura - nivel1_surface.get_width()) // 2, (tela_altura - nivel1_surface.get_height()) // 2))
            pygame.draw.rect(tela, (255, 0, 0), (tela_largura - 200, 10, 190, 50))
            texto_fechar = fonte.render("Fechar", True, (255, 255, 255))
            tela.blit(texto_fechar, (tela_largura - 190, 20))

        for evento in pygame.event.get():
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1: 
                    if tela_largura - 200 <= evento.pos[0] <= tela_largura - 10 and 10 <= evento.pos[1] <= 60:
                        imagem_aberta = False 


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

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:  # Botão esquerdo do mouse
                if not craft_aberto:
                    coletar_madeira()
                    coletar_pedra()
                    coletar_ferro()
                if craft_aberto:
                    if tela_largura - 400 <= evento.pos[0] <= tela_largura and 0 <= evento.pos[1] <= tela_altura:
                        comprar_item("Picareta de Madeira")
                        comprar_item("Picareta de Pedra")
                        comprar_item("Picareta de Ferro")
                        comprar_item("Prefeitura")
                        comprar_item("Muro")
                        comprar_item("Bunker")
                        if "Picareta de Madeira" in itens_comprados or "Picareta de Pedra" in itens_comprados:
                            possui_picareta_de_pedra = True

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

    if not craft_aberto:
        desenhar_cenario(cenario_atual)
        desenhar_botão_craft()
    else:
        desenhar_interface_craft()
        desenhar_nivel()

    if aviso and time.time() - tempo_do_aviso >= aviso_duracao:
        aviso = ""

    # Verifique se a imagem da prefeitura está aberta e renderize-a

    pygame.display.update()

# Finaliza o jogo
pygame.quit()