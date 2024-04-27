from joga_da_velha import criaBoard, fazMovimento, getInputValido, printBoard, verificaGanhador, verificaMovimento

from minimax import movimentoIA

jogador = 0 # jogador 1
board = criaBoard()
ganhador = verificaGanhador(board)
while(not ganhador):
    printBoard(board)
    print("=====================")

    if(jogador == 0):
        i, j = movimentoIA(board, jogador)
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

print("=====================")
printBoard(board)    
print("Ganhador = ", ganhador)
print("=====================")