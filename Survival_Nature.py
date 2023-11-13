import pygame
import random
import time
import datetime
import sys

# Inicialização do Pygame
pygame.init()

# Inicialização do Pygame Mixer
pygame.mixer.init()

# Configurações da tela
tela_largura = 1200
tela_altura = 900
tela = pygame.display.set_mode((tela_largura, tela_altura))
pygame.display.set_caption("Survive Nature")

# Carregando a trilha sonora
pygame.mixer.music.load("trilha-sonora.mp3")

# Carregando imagens
cenario1 = pygame.image.load("cenario1.png")
cenario2 = pygame.image.load("cenario2.png")
cenario3 = pygame.image.load("cenario3.png")
cenario4 = pygame.image.load("cenario4.png")
jogador = pygame.image.load("jogador.png")
jogador_correndo = pygame.image.load("jogador_correndo.png")
arvore = pygame.image.load("arvore.png")
pedra_img = pygame.image.load("pedra.png")
ferro_img = pygame.image.load("ferro.png")
nivel1_img = pygame.image.load("Nivel1.png")
nivel2_img = pygame.image.load("Nivel2.png")
nivel3_img = pygame.image.load("Nivel3.png")
Imagem_Inicial = pygame.image.load("Tela_Inicial.png")


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

tempo_maximo = datetime.timedelta(minutes=5)
tempo_inicial = datetime.datetime.now()
tempo_atual = datetime.datetime.now()
nivel = 1

# Variáveis de recursos
recursos = {
    "madeira": 0,
    "pedra": 0,
    "ferro": 0,
}

# Fonte para exibir informações na tela
fonte = pygame.font.Font(None, 36)

# Velocidade do jogador
velocidade = 10

estado_movimento = "parado"
tempo_ultima_atualizacao = pygame.time.get_ticks()
intervalo_animacao = 2
jogador_ativo = jogador

# Variáveis para controle de árvores, pedras e ferro
arvores = []
pedras = []
ferro = []

# Função para calcular o tempo restante
def calcular_tempo_restante():
    tempo_decorrido = tempo_atual - tempo_inicial
    tempo_restante = tempo_maximo - tempo_decorrido
    return tempo_restante

# Função para verificar o Game Over
def verificar_game_over():
    tempo_restante = calcular_tempo_restante()
    if tempo_restante.total_seconds() <= 0:
        return True
    return False

def exibir_cronometro(tempo_atual):
        tempo_restante = calcular_tempo_restante()
        minutos = tempo_restante.seconds // 60
        segundos = tempo_restante.seconds % 60
        tempo_formatado = f"{minutos:02d}:{segundos:02d}"
        texto_cronometro = fonte.render(f"Tempo Restante: {tempo_formatado}", True, (255, 255, 255))
        tela.blit(texto_cronometro, (10, tela_altura - 40))


game_over = False
def mostrar_game_over():
    global game_over
    while game_over:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                # Reiniciar o jogo
                recursos["madeira"] = 40
                recursos["pedra"] = 40
                recursos["ferro"] = 40
                itens_comprados.clear()
                possui_picareta_de_pedra = False
                possui_picareta_de_ferro = False
                item_selecionado = None
                craft_aberto = False
                prefeitura_comprada = False
                imagem_aberta = False
                nivel = 1
                tempo_inicial = datetime.datetime.now() + tempo_maximo
                game_over = False  # Isso encerrará o loop do Game Over

        tela.fill((0, 0, 0))  # Preenche a tela de preto
        texto_game_over = fonte.render("Game Over", True, (255, 0, 0))
        tela.blit(texto_game_over, ((tela_largura - texto_game_over.get_width()) // 2, (tela_altura - texto_game_over.get_height()) // 2))
        texto_tentar_novamente = fonte.render("Clique para Tentar Novamente", True, (255, 255, 255))
        tela.blit(texto_tentar_novamente, ((tela_largura - texto_tentar_novamente.get_width()) // 2, (tela_altura // 2 + 50)))
        pygame.display.update()

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
    "Prefeitura": {"madeira": 20, "pedra": 10},
    "Muro": {"madeira": 30, "pedra": 15, "ferro": 10},
    "Bunker": {"madeira": 50, "pedra": 30, "ferro": 30},
}

itens_disponíveis = {
    "Picareta de Madeira": {"madeira": 5},
    "Picareta de Pedra": {"pedra": 10 },
    "Picareta de Ferro": {"ferro": 10},
    "Prefeitura": {"madeira": 20, "pedra": 10},
    "Muro": {"madeira": 25, "pedra": 25, "ferro": 15},
    "Bunker": {"madeira": 45, "pedra": 35, "ferro": 40},
}

itens_comprados = {}
possui_picareta_de_pedra = False  # Variável para verificar se o jogador possui a picareta de pedra
possui_picareta_de_ferro = False  # Variável para verificar se o jogador possui a picareta de ferro
item_selecionado = None
craft_aberto = False
prefeitura_comprada = False
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
    tela.blit(jogador_ativo, (jogador_x, jogador_y))

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
nivel_equipamento = 0
def comprar_item(item):
    global item_selecionado, recursos, aviso, possui_picareta_de_pedra, imagem_aberta, nivel_equipamento
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
                if item == "Picareta de Madeira":
                    nivel_equipamento = 1
                if item == "Picareta de Pedra":
                    nivel_equipamento = 2
                if item == "Picareta de Ferro":
                    possui_picareta_de_ferro = True
                    nivel_equipamento = 3
                

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

def desenhar_nivel():
    global nivel1_img, nivel2_img, nivel3_img, nivel, tempo_inicial, tempo_maximo

    if "Prefeitura" in itens_comprados and nivel == 1:
            tela.blit(nivel1_img, ((tela_largura - nivel1_img.get_width()) // 2, (tela_altura - nivel1_img.get_height()) // 2))
            pygame.draw.rect(tela, (255, 0, 0), (tela_largura - 200, 10, 190, 50))
            texto_fechar = fonte.render("Fechar", True, (255, 255, 255))
            tela.blit(texto_fechar, (tela_largura - 190, 20))

            for evento in pygame.event.get():
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1:
                        if tela_largura - 200 <= evento.pos[0] <= tela_largura - 10 and 10 <= evento.pos[1] <= 60:
                            nivel1_img = None
                            nivel = 2

    if "Muro" in itens_comprados and nivel == 2:
            tela.blit(nivel2_img, ((tela_largura - nivel2_img.get_width()) // 2, (tela_altura - nivel2_img.get_height()) // 2))
            pygame.draw.rect(tela, (255, 0, 0), (tela_largura - 200, 10, 190, 50))
            texto_fechar = fonte.render("Fechar", True, (255, 255, 255))
            tela.blit(texto_fechar, (tela_largura - 190, 20))

            for evento in pygame.event.get():
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1:
                        if tela_largura - 200 <= evento.pos[0] <= tela_largura - 10 and 10 <= evento.pos[1] <= 60:
                            nivel2_img = None
                            nivel = 3
    
    if "Bunker" in itens_comprados and nivel == 3:
            tela.blit(nivel3_img, ((tela_largura - nivel3_img.get_width()) // 2, (tela_altura - nivel3_img.get_height()) // 2))
            pygame.draw.rect(tela, (255, 0, 0), (tela_largura - 200, 10, 190, 50))
            texto_fechar = fonte.render("Fechar", True, (255, 255, 255))
            tela.blit(texto_fechar, (tela_largura - 190, 20))

            for evento in pygame.event.get():
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1:
                        if tela_largura - 200 <= evento.pos[0] <= tela_largura - 10 and 10 <= evento.pos[1] <= 60:
                            nivel3_img = None
                            nivel = 4
        

def desenhar_nivel_atual(nivel):
    texto_nivel = fonte.render(f"Nível {nivel}", True, (255, 255, 255))
    tela.blit(texto_nivel, ((tela_largura - texto_nivel.get_width()) // 2, 10))

# Inicialmente, mostramos o primeiro cenário
cenario_atual = cenario1
gerar_arvores(50, 100)
gerar_pedras(100, 100)
gerar_ferro(200, 100)
picareta_madeira = False

# Loop principal
executando = True
cronometro_reiniciado1 = False
cronometro_reiniciado2 = False
tela_inicial = True
pygame.mixer.music.play(-1)
while executando:
    while not game_over:   
        if tela_inicial == False:
            if nivel == 4 :
                tela.fill((0, 0, 0))  # Preenche a tela de preto
                texto_credito = fonte.render("Muito Obrigado por Jogar", True, (255, 0, 0))
                tela.blit(texto_credito, ((tela_largura - texto_credito.get_width()) // 2, (tela_altura - texto_credito.get_height()) // 2))
                texto_creditos2 = fonte.render("Desenvolvedor : Felippe Wurcker Goe Mazuca ", True, (255, 255, 255))
                tela.blit(texto_creditos2, ((tela_largura - texto_creditos2.get_width()) // 2, (tela_altura // 2 + 50)))
                pygame.display.update()   
                pygame.time.delay(1000) 
                        
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    executando = False
                    game_over = True
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
                                if nivel_equipamento == 1:
                                    comprar_item("Picareta de Pedra")
                                if nivel_equipamento == 2:
                                    comprar_item("Picareta de Ferro")
                                if nivel_equipamento == 3:
                                    comprar_item("Prefeitura")
                                if nivel == 2:
                                    comprar_item("Muro")
                                if nivel == 3:
                                    comprar_item("Bunker")
                                if "Picareta de Madeira" in itens_comprados or "Picareta de Pedra" in itens_comprados:
                                    possui_picareta_de_pedra = True

            # Verifica o estado da tecla pressionada
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    estado_movimento = "correndo_esquerda"
                elif evento.key == pygame.K_d:
                    estado_movimento = "correndo_direita"

            # Verifica o estado da tecla solta
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_a or evento.key == pygame.K_d:
                    estado_movimento = "parado"
            
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_a] and jogador_x > limite_esquerda_cenario:
                jogador_x -= velocidade
                estado_movimento = "correndo"
            if teclas[pygame.K_d] and jogador_x < limite_direita_cenario:
                jogador_x += velocidade
                estado_movimento = "correndo"
            else:
                estado_movimento = "parado"
            
            # Atualizando a tela
            tela.fill((0, 0, 0))
        
           # Verificando e alternando a imagem do jogador
            tempo_atual = pygame.time.get_ticks()
            if estado_movimento == "correndo" and tempo_atual - tempo_ultima_atualizacao > intervalo_animacao:
                jogador_ativo = jogador_correndo
                tempo_ultima_atualizacao = tempo_atual
            else:
                jogador_ativo = jogador

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

            # Atualiza o tempo atual
            tempo_atual = datetime.datetime.now()

            if not craft_aberto:
                desenhar_cenario(cenario_atual)
                desenhar_botão_craft()
            else:
                desenhar_interface_craft()
                desenhar_nivel()

            if aviso and time.time() - tempo_do_aviso >= aviso_duracao:
                aviso = ""

            # Exibir o cronômetro na tela
            exibir_cronometro(tempo_atual)

            # Desenhar o nível atual na tela
            desenhar_nivel_atual(nivel)

            if nivel == 2 and not cronometro_reiniciado1:
                tempo_inicial = datetime.datetime.now()
                cronometro_reiniciado1 = True
            
            if nivel == 3 and not cronometro_reiniciado2:
                tempo_inicial = datetime.datetime.now()
                cronometro_reiniciado2 = True

            if verificar_game_over():
                game_over = True

            pygame.display.update()

        if tela_inicial == True:
            tela.blit(Imagem_Inicial, ((tela_largura - Imagem_Inicial.get_width()) // 2, (tela_altura - Imagem_Inicial.get_height()) // 2))
            pygame.draw.rect(tela, (255, 0, 0), (tela_largura - 200, 10, 190, 50))
            texto_fechar = fonte.render("Fechar", True, (255, 255, 255))
            tela.blit(texto_fechar, (tela_largura - 190, 20))
            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1:
                        if tela_largura - 200 <= evento.pos[0] <= tela_largura - 10 and 10 <= evento.pos[1] <= 60:
                            Imagem_Inicial = None
                            tela_inicial = False
    mostrar_game_over()

    # Finaliza o jogo
pygame.quit()