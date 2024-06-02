import pygame
import sys
import random
from button import Button

from joga_da_velha import criaBoard, fazMovimento, getInputValido, printBoard, verificaGanhador, verificaMovimento
from minimax import movimentoIA

pygame.font.init()

BG = pygame.image.load("assets/Background.png")

dificuldade = ["NONE", "NONE"]
modo_jogador = ["NONE", "NONE"]


# Função para desenhar o tabuleiro
def draw_board(win, board, offset_x, offset_y):
    tamanho = 600 / 3

    for i in range(1, 3):
        pygame.draw.line(win, (0, 0, 0), (offset_x, offset_y + i * tamanho), (offset_x + 600, offset_y + i * tamanho), 3)
        pygame.draw.line(win, (0, 0, 0), (offset_x + i * tamanho, offset_y), (offset_x + i * tamanho, offset_y + 600), 3)

    for i in range(3):
        for j in range(3):
            font = pygame.font.SysFont("comicsans", 100)
            x = offset_x + j * tamanho
            y = offset_y + i * tamanho
            text = font.render(board[i][j], 1, (128, 0, 0))
            win.blit(text, ((x + 75), (y + 75)))

# Função para desenhar o placar
def draw_score(win, placar, offset_x):
    font = pygame.font.SysFont("comicsans", 50)
    score_text = font.render(f"X: {placar[0]}  O: {placar[1]}", 1, (0, 0, 0))
    text_width = score_text.get_width()
    win.blit(score_text, ((800 - text_width) // 2, 750))

# Função para redesenhar a janela
def redraw_window(win, board, placar, offset_x, offset_y):
    win.fill((255, 255, 255))
    draw_board(win, board, offset_x, offset_y)
    draw_score(win, placar, offset_x)
    pygame.display.update()

def main():
    win = pygame.display.set_mode((800, 900))  # 
    pygame.display.set_caption("Jogo Da Velha")
    win.fill("white")

    placar = [0, 0]  # Placar para os dois jogadores

    offset_x = 100  # Deslocamento horizontal para centralizar o tabuleiro
    offset_y = 100  # Deslocamento vertical para centralizar o tabuleiro

    running = True
    while running:
        board = criaBoard()
        redraw_window(win, board, placar, offset_x, offset_y)

        count = 0
        jogador = 0  # jogador 1
        ganhador = verificaGanhador(board)
        while not ganhador and running:
            printBoard(board)
            print("=====================")

            if modo_jogador[jogador] == "HUMANO":
                jogou = False
                while not jogou:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            return
                        elif event.type == pygame.MOUSEBUTTONUP:
                            pos = pygame.mouse.get_pos()
                            if offset_y < pos[1] < offset_y + 600 and offset_x < pos[0] < offset_x + 600:  # Certifique-se de que o clique está dentro da área do tabuleiro
                                i = int((pos[1] - offset_y) / 200)
                                j = int((pos[0] - offset_x) / 200)
                                jogou = True
            elif modo_jogador[jogador] == "I.A" and dificuldade[1] == "FACIL":
                i, j = movimentoIA(board, ((jogador + 1) % 2))
            elif modo_jogador[jogador] == "I.A" and dificuldade[1] == "MEDIO":
                i = random.randint(0,2)
                j = random.randint(0,2)
            elif modo_jogador[jogador] == "I.A" and dificuldade[1] == "IMPOSSIVEL":
                i, j = movimentoIA(board, jogador)

            if verificaMovimento(board, i, j):
                fazMovimento(board, i, j, jogador)
                jogador = (jogador + 1) % 2
            else:
                print("A posição informada já está ocupada")

            ganhador = verificaGanhador(board)
            redraw_window(win, board, placar, offset_x, offset_y)
            count += 1

        printBoard(board)

        if ganhador == "0":
            placar[1] += 1
        elif ganhador == "X":
            placar[0] += 1

        redraw_window(win, board, placar, offset_x, offset_y)

        pygame.time.wait(2000)  # Esperar 2 segundos antes de reiniciar

        # Reiniciar o tabuleiro para o próximo jogo
        board = criaBoard()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

    pygame.quit()
    sys.exit()

def player_select():
    win = pygame.display.set_mode((1280, 720))
    font = pygame.font.SysFont("comicsans", 50)
    
    while True:
        win.blit(BG, (0, 0))

        PLAYER_MOUSE_POS = pygame.mouse.get_pos()

        PLAYER_TEXT = font.render("SELECIONE O PLAYER", True, "#b68f40")
        PLAYER_RECT = PLAYER_TEXT.get_rect(center=(640, 100))

        HVSH_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 250), 
                            text_input="HUMANO VS HUMANO", font=font, base_color="#d7fcd4", hovering_color="White")
        HVSIA_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="HUMANO VS I.A", font=font, base_color="#d7fcd4", hovering_color="White")
        IAVSIA_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 550), 
                            text_input="I.A VS I.A", font=font, base_color="#d7fcd4", hovering_color="White")

        win.blit(PLAYER_TEXT, PLAYER_RECT)

        for button in [HVSH_BUTTON, HVSIA_BUTTON, IAVSIA_BUTTON]:
            button.changeColor(PLAYER_MOUSE_POS)
            button.update(win)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if HVSH_BUTTON.checkForInput(PLAYER_MOUSE_POS):
                    modo_jogador[0] = "HUMANO"
                    modo_jogador[1] = "HUMANO"
                    main()
                if HVSIA_BUTTON.checkForInput(PLAYER_MOUSE_POS):
                    modo_jogador[0] = "HUMANO"
                    modo_jogador[1] = "I.A"
                    dificulty_select()
                if IAVSIA_BUTTON.checkForInput(PLAYER_MOUSE_POS):
                    modo_jogador[0] = "I.A"
                    modo_jogador[1] = "I.A"
                    dificulty_select()

        pygame.display.update()


def dificulty_select():
    win = pygame.display.set_mode((1280, 720))
    font = pygame.font.SysFont("comicsans", 60)
    
    while True:
        win.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = font.render("SELECIONE A DIFICULDADE", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        FACIL_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 250), 
                            text_input="FABRÍCIO", font=font, base_color="#d7fcd4", hovering_color="White")
        MEDIO_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="MÉDIO", font=font, base_color="#d7fcd4", hovering_color="White")
        IMPOSSIVEL_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 550), 
                            text_input="IMPOSSÍVEL", font=font, base_color="#d7fcd4", hovering_color="White")

        win.blit(MENU_TEXT, MENU_RECT)

        for button in [FACIL_BUTTON, MEDIO_BUTTON, IMPOSSIVEL_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(win)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if FACIL_BUTTON.checkForInput(MENU_MOUSE_POS):
                    dificuldade[1] = "FACIL"
                    main()
                if MEDIO_BUTTON.checkForInput(MENU_MOUSE_POS):
                    dificuldade[1] = "MEDIO"
                    main()
                if IMPOSSIVEL_BUTTON.checkForInput(MENU_MOUSE_POS):
                    dificuldade[1] = "IMPOSSIVEL"
                    main()

        pygame.display.update()

def main_menu():
    win = pygame.display.set_mode((1280, 720))
    font = pygame.font.SysFont("comicsans", 100)
    
    while True:
        win.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = font.render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=font, base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 400), 
                            text_input="QUIT", font=font, base_color="#d7fcd4", hovering_color="White")

        win.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(win)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    player_select()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
