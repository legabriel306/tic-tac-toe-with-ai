import pygame
import sys
import random
import requests
from button import Button

from joga_da_velha import criaBoard, fazMovimento, getInputValido, printBoard, verificaGanhador, verificaMovimento
from minimax import movimentoIA

pygame.font.init()

BG = pygame.image.load("assets/Background.png")

dificuldade = ["NONE", "NONE"]
modo_jogador = ["NONE", "NONE"]
nome_jogadores = ["NONE", "NONE"]

API_URL = "http://127.0.0.1:5000"

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def get_ranking():
    try:
        response = requests.get(f"{API_URL}/ranking")
        response.raise_for_status()
        ranking = response.json()
        ranking.sort(key=lambda player: player['score'], reverse=True)  # Ordena por pontuação
        return ranking
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter ranking: {e}")
        return []

def post_game_result(jogador1, jogador2, vencedor):
    url = f"{API_URL}/ranking"
    payload = {"jogador1": jogador1, "jogador2": jogador2, "vencedor": vencedor}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print(f"Resultado do jogo registrado com sucesso.")
    else:
        print(f"Falha ao registrar o resultado do jogo. Status Code: {response.status_code}")

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

def draw_score(win, placar, offset_x):
    font = pygame.font.SysFont("comicsans", 50)
    score_text = font.render(f"X: {placar[0]}  O: {placar[1]}", 1, (0, 0, 0))
    text_width = score_text.get_width()
    win.blit(score_text, ((800 - text_width) // 2, 750))

def draw_ranking(win, ranking, offset_x, offset_y):
    font = pygame.font.SysFont("comicsans", 50)
    for idx, player in enumerate(ranking):
        rank_text = font.render(f"{idx+1}. {player['name']} - {player['score']}", 1, (255, 255, 255))
        win.blit(rank_text, (offset_x, offset_y + idx * 60))

def redraw_window(win, board, placar, offset_x, offset_y):
    win.fill((255, 255, 255))

    draw_board(win, board, offset_x, offset_y)
    draw_score(win, placar, offset_x)

    font = pygame.font.SysFont("comicsans", 50)
    PLAY_MOUSE_POS = pygame.mouse.get_pos()
    PLAY_BACK = Button(image=None, pos=(100, 100),
                       text_input="BACK", font=font, base_color="#000000", hovering_color="Green")

    PLAY_BACK.changeColor(PLAY_MOUSE_POS)
    PLAY_BACK.update(win)
    pygame.display.update()


    pygame.display.update()

def main():
    win = pygame.display.set_mode((800, 900))
    pygame.display.set_caption("Jogo Da Velha")
    win.fill("white")
    font = pygame.font.SysFont("comicsans", 50)

    placar = [0, 0]
    offset_x = 100
    offset_y = 100

    print(nome_jogadores[0], nome_jogadores[1])

    running = True
    while running:
        board = criaBoard()
        redraw_window(win, board, placar, offset_x, offset_y)

        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        PLAY_BACK = Button(image=None, pos=(100, 100),
                           text_input="BACK", font=font, base_color="#000000", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(win)
        pygame.display.update()

        alternar = 0

        count = 0
        jogador = 0
        ganhador = verificaGanhador(board)
        while not ganhador and running:

            PLAY_MOUSE_POS = pygame.mouse.get_pos()
            PLAY_BACK = Button(image=None, pos=(100, 100),
                               text_input="BACK", font=font, base_color="#000000", hovering_color="Green")

            PLAY_BACK.changeColor(PLAY_MOUSE_POS)
            PLAY_BACK.update(win)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                        main_menu()

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
                            if offset_y < pos[1] < offset_y + 600 and offset_x < pos[0] < offset_x + 600:
                                i = int((pos[1] - offset_y) / 200)
                                j = int((pos[0] - offset_x) / 200)
                                jogou = True
                            if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                                main_menu()
            elif modo_jogador[jogador] == "I.A" and dificuldade[1] == "FACIL":
                i, j = movimentoIA(board, ((jogador + 1) % 2))
            elif modo_jogador[jogador] == "I.A" and dificuldade[1] == "MEDIO":
                if alternar:
                    i = random.randint(0,2)
                    j = random.randint(0,2)
                else:
                    i, j = movimentoIA(board, jogador)

                alternar = (alternar + 1) % 2
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
            post_game_result(nome_jogadores[0], nome_jogadores[1], nome_jogadores[1])
        elif ganhador == "X":
            placar[0] += 1
            post_game_result(nome_jogadores[0], nome_jogadores[1], nome_jogadores[0])

        redraw_window(win, board, placar, offset_x, offset_y)

        pygame.time.wait(2000)

        board = criaBoard()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

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
        BACK_BUTTON = Button(image=None, pos=(100, 100),
                            text_input="VOLTAR", font=get_font(20), base_color="#ffffff", hovering_color="Green")

        BACK_BUTTON.changeColor(PLAYER_MOUSE_POS)
        BACK_BUTTON.update(win)

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
                    name_input_screen_HVSH()
                if HVSIA_BUTTON.checkForInput(PLAYER_MOUSE_POS):
                    modo_jogador[0] = "HUMANO"
                    modo_jogador[1] = "I.A"
                    name_input_screen_HVSIA()
                if IAVSIA_BUTTON.checkForInput(PLAYER_MOUSE_POS):
                    modo_jogador[0] = "I.A"
                    modo_jogador[1] = "I.A"
                    dificulty_select()
                if BACK_BUTTON.checkForInput(PLAYER_MOUSE_POS):
                    main_menu()

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
                            text_input="FACIL", font=font, base_color="#d7fcd4", hovering_color="White")
        MEDIO_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                            text_input="MÉDIO", font=font, base_color="#d7fcd4", hovering_color="White")
        IMPOSSIVEL_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 550),
                            text_input="IMPOSSÍVEL", font=font, base_color="#d7fcd4", hovering_color="White")
        BACK_BUTTON = Button(image=None, pos=(100, 100),
                            text_input="VOLTAR", font=get_font(20), base_color="#ffffff", hovering_color="Green")

        BACK_BUTTON.changeColor(MENU_MOUSE_POS)
        BACK_BUTTON.update(win)

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
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    player_select()

        pygame.display.update()

def players_ranking():
    win = pygame.display.set_mode((1280, 720))
    font = pygame.font.SysFont("comicsans", 100)

    while True:
        win.blit(BG, (0, 0))

        RANKING_MOUSE_POS = pygame.mouse.get_pos()

        RANKING_TEXT = font.render("RANKING", True, "#b68f40")
        RANKING_RECT = RANKING_TEXT.get_rect(center=(640, 100))

        BACK_BUTTON = Button(image=None, pos=(100, 100),
                            text_input="VOLTAR", font=get_font(20), base_color="#ffffff", hovering_color="Green")

        BACK_BUTTON.changeColor(RANKING_MOUSE_POS)
        BACK_BUTTON.update(win)

        win.blit(RANKING_TEXT, RANKING_RECT)

        ranking = get_ranking()
        draw_ranking(win, ranking, 100, 200)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(RANKING_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def name_input_screen_HVSH():
    pygame.init()
    win = pygame.display.set_mode((1280, 720))
    font = pygame.font.SysFont("comicsans", 60)
    small_font = pygame.font.SysFont("comicsans", 40)

    input_box1 = pygame.Rect(440, 250, 400, 50)
    input_box2 = pygame.Rect(440, 350, 400, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color1 = color_inactive
    color2 = color_inactive
    active1 = False
    active2 = False
    text1 = ''
    text2 = ''
    done = False

    start_button = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 500),
                          text_input="JOGAR", font=font, base_color="#d7fcd4", hovering_color="White")


    BACK_BUTTON = Button(image=None, pos=(100, 100),
                        text_input="VOLTAR", font=get_font(20), base_color="#ffffff", hovering_color="Green")



    while not done:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box1.collidepoint(event.pos):
                    active1 = not active1
                else:
                    active1 = False
                if input_box2.collidepoint(event.pos):
                    active2 = not active2
                else:
                    active2 = False
                color1 = color_active if active1 else color_inactive
                color2 = color_active if active2 else color_inactive
                if start_button.checkForInput(pygame.mouse.get_pos()):
                    if (text1 and text2) and (text1 != text2):
                        done = True
                        main()
                if BACK_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    player_select()
            if event.type == pygame.KEYDOWN:
                if active1:
                    if event.key == pygame.K_RETURN:
                        active1 = False
                    elif event.key == pygame.K_BACKSPACE:
                        text1 = text1[:-1]
                    else:
                        text1 += event.unicode
                if active2:
                    if event.key == pygame.K_RETURN:
                        active2 = False
                    elif event.key == pygame.K_BACKSPACE:
                        text2 = text2[:-1]
                    else:
                        text2 += event.unicode

        win.fill((30, 30, 30))
        txt_surface1 = font.render(text1, True, color1)
        txt_surface2 = font.render(text2, True, color2)
        width1 = max(400, txt_surface1.get_width() + 10)
        input_box1.w = width1
        width2 = max(400, txt_surface2.get_width() + 10)
        input_box2.w = width2
        win.blit(txt_surface1, (input_box1.x + 10, input_box1.y - 25))
        win.blit(txt_surface2, (input_box2.x + 10, input_box2.y - 25))
        pygame.draw.rect(win, color1, input_box1, 2)
        pygame.draw.rect(win, color2, input_box2, 2)

        prompt1 = small_font.render("Jogador 1:", True, (255, 255, 255))
        prompt2 = small_font.render("Jogador 2:", True, (255, 255, 255))
        win.blit(prompt1, (220, 250))
        win.blit(prompt2, (220, 350))

        BACK_BUTTON.changeColor(pygame.mouse.get_pos())
        BACK_BUTTON.update(win)

        start_button.changeColor(pygame.mouse.get_pos())
        start_button.update(win)

        pygame.display.flip()

        nome_jogadores[0] = text1
        nome_jogadores[1] = text2

    return text1, text2

def name_input_screen_HVSIA():
    pygame.init()
    win = pygame.display.set_mode((1280, 720))
    font = pygame.font.SysFont("comicsans", 60)
    small_font = pygame.font.SysFont("comicsans", 40)

    input_box1 = pygame.Rect(440, 250, 400, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color1 = color_inactive
    active1 = False
    text1 = ''
    done = False

    start_button = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 500),
                          text_input="JOGAR", font=font, base_color="#d7fcd4", hovering_color="White")

    BACK_BUTTON = Button(image=None, pos=(100, 100),
                        text_input="VOLTAR", font=get_font(20), base_color="#ffffff", hovering_color="Green")



    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box1.collidepoint(event.pos):
                    active1 = not active1
                else:
                    active1 = False

                color1 = color_active if active1 else color_inactive

                if start_button.checkForInput(pygame.mouse.get_pos()):
                    if text1:
                        done = True
                        dificulty_select()

                if BACK_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    player_select()
            if event.type == pygame.KEYDOWN:
                if active1:
                    if event.key == pygame.K_RETURN:
                        active1 = False
                    elif event.key == pygame.K_BACKSPACE:
                        text1 = text1[:-1]
                    else:
                        text1 += event.unicode

        win.fill((30, 30, 30))
        txt_surface1 = font.render(text1, True, color1)
        width1 = max(400, txt_surface1.get_width() + 10)
        input_box1.w = width1
        win.blit(txt_surface1, (input_box1.x + 10, input_box1.y - 25))
        pygame.draw.rect(win, color1, input_box1, 2)

        prompt1 = small_font.render("Jogador 1:", True, (255, 255, 255))
        win.blit(prompt1, (220, 250))

        start_button.changeColor(pygame.mouse.get_pos())
        start_button.update(win)

        BACK_BUTTON.changeColor(pygame.mouse.get_pos())
        BACK_BUTTON.update(win)

        pygame.display.flip()

        nome_jogadores[0] = text1
        nome_jogadores[1] = "NONE"

    return text1



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
        RANKING_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                            text_input="RANK", font=font, base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                            text_input="QUIT", font=font, base_color="#d7fcd4", hovering_color="White")

        win.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, RANKING_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    player_select()
                if RANKING_BUTTON.checkForInput(MENU_MOUSE_POS):
                    players_ranking()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
