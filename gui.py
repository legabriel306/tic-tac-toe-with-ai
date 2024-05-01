import pygame
import random

from joga_da_velha import criaBoard, fazMovimento, getInputValido, printBoard, verificaGanhador, verificaMovimento

from minimax import movimentoIA

pygame.font.init()

def draw_board(win, board):
    height = 600
    width = 600
    tamanho = 600/3

    for i in range(1, 3):
        pygame.draw.line(win, (0, 0 ,0), (0, i *  tamanho), (width, i * tamanho), 3)
        pygame.draw.line(win, (0, 0 ,0), (i * tamanho, 0), (i * tamanho, height), 3)

    for i in range(3):
        for j in range(3):
            font = pygame.font.SysFont("comicsans", 100)

            x = j * tamanho
            y = i * tamanho

            text = font.render(board[i][j], 1, (128, 0, 0))
            win.blit(text, ((x + 75), (y + 75)))

def  redraw_window(win, board):
    win.fill((255, 255, 255))
    draw_board(win, board)

def main():
    win = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Jogo Da Velha")

    board = criaBoard()

    redraw_window(win, board)
    pygame.display.update()

    count = 0
    jogador = 0 # jogador 1
    ganhador = verificaGanhador(board)
    while(not ganhador):
        printBoard(board)
        print("=====================")

        if(jogador == 0):
            if (count == 0):
                i = int(random.choice([0,1,2]))
                j = int(random.choice([0,1,2]))
            else:
                i, j = movimentoIA(board, jogador)

            '''
            jogou = False
            while(not jogou):
                for event in pygame.event.get():
                    if(event.type == pygame.QUIT):
                        return
                    elif(event.type == pygame.MOUSEBUTTONUP):
                        pos = pygame.mouse.get_pos()
                        i = int(pos[1]/200)
                        j = int(pos[0]/200)
                        jogou = True'''
            
        else:
            i, j = movimentoIA(board, jogador)
            #i = getInputValido("Digite a linha: ")
            #j = getInputValido("Digite a coluna: ")

        if(verificaMovimento(board, i,j)):
            fazMovimento(board, i, j, jogador)
            jogador = (jogador+1)%2
        else:
            print("A posição informada ja esta ocupada")

        ganhador = verificaGanhador(board)
        redraw_window(win, board)
        pygame.display.update()
        count = count + 1

    printBoard(board)

    # Se apertar no x sai da tela
    while(True):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                return

main()