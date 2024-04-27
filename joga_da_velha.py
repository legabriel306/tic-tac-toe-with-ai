branco = " "
token = ["X", "0"]

#Cria a tabela utilizada no jogo da velha
# Board = tabela/tabuleiro
def criaBoard():
    board = [
        [branco, branco, branco],
        [branco, branco, branco],
        [branco, branco, branco],
    ]

    return board

# apresenta a tabela do jogo
def printBoard(board):
    for i in range(3):
        print("|".join(board[i]))
        if(i < 2):
            print("------")

# Recebe um input do teclado e valida para ver se pode ser utilizado
def getInputValido(mensagem):
    try:
        n = int(input(mensagem))
        if(n >= 1 and n <= 3):
            return n - 1
        else:
            print("Número precisa estar entre 1 e 3")
            return getInputValido(mensagem)
    except:
        print("Numero não valido")
        return getInputValido(mensagem)


# Verifica se o movimento pode ser realizado
def verificaMovimento(board, i, j):
    if(board[i][j] == branco):
        return True
    else:
        return False

# Realiza o movimento
def fazMovimento(board, i, j, jogador):
    board[i][j] = token[jogador]

# verifica se o jogo já acabou e se temos um vencedor ou um empate
def verificaGanhador(board):
    # linhas
    for i in range(3):
        if(board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] != branco):
            return board[i][0]

    # coluna
    for i in range(3):
        if(board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[0][i] != branco):
            return board[0][i]
    
    #Diagonal principal
    if(board[0][0] != branco and board[0][0] ==  board[1][1] and board[1][1] == board[2][2]):
        return board[0][0]
    
    #Diagonal secundaria
    if(board[0][2] != branco and board[0][2] ==  board[1][1] and board[1][1] == board[2][0]):
        return board[0][2]
    
    for i in range(3):
        for j in range(3):
            if(board[i][j] == branco):
                return False

    return "EMPATE"

