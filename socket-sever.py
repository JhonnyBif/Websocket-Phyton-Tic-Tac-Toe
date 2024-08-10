import socket
import threading

# Configurações do servidor
HOST = '' #YOUR IP  
PORT = 0000 ## YOUR PORT        

def reset_board():
    return [[' ' for _ in range(3)] for _ in range(3)]

board = reset_board()
current_player = 'X'
game_over = False

def print_board():
    for row in board:
        print('|'.join(row))
        print('-' * 5)
    print('\n')


def check_winner():
    # Verifica linhas
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return row[0]

    # Verifica colunas
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return board[0][col]

    # Verifica diagonais
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]

    return None

def handle_client(conn, addr, player):
    global current_player, game_over, board
    conn.sendall(f"Você é o jogador {player}\n".encode())

    while True:
        if game_over:
            conn.sendall("O jogo acabou!\n".encode())
            move = conn.recv(1024).decode().strip()
            if move.lower() == 'replay':
                if player == 'X':
                    board = reset_board()
                    current_player = 'X'
                    game_over = False
                    conn.sendall("Novo jogo iniciado! Você é o jogador X\n".encode())
                else:
                    conn.sendall("Aguardando o jogador X iniciar um novo jogo...\n".encode())
            else:
                conn.sendall("Aguarde o reinício do jogo ou envie 'replay' para jogar novamente.\n".encode())
            continue

        if current_player == player:
            conn.sendall("Sua vez de jogar. Envie sua jogada no formato linha,coluna:\n".encode())
            move = conn.recv(1024).decode().strip()
            if not move:
                continue
            try:
                row, col = map(int, move.split(','))
                if row < 0 or row > 2 or col < 0 or col > 2 or board[row][col] != ' ':
                    conn.sendall("Movimento inválido! Tente novamente.\n".encode())
                else:
                    board[row][col] = player
                    winner = check_winner()
                    if winner:
                        game_over = True
                        conn.sendall(f"Jogador {winner} venceu! Envie 'replay' para jogar novamente.\n".encode())
                    elif all(cell != ' ' for row in board for cell in row):
                        game_over = True
                        conn.sendall("Empate! Envie 'replay' para jogar novamente.\n".encode())
                    else:
                        current_player = 'O' if player == 'X' else 'X'
                        print_board()
            except ValueError:
                conn.sendall("Formato inválido! Use linha,coluna. Tente novamente.\n".encode())
        else:
            conn.sendall("Aguarde sua vez...\n".encode())

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor ouvindo em {HOST}:{PORT}")
        
        conn1, addr1 = s.accept()
        print(f"Conectado com {addr1}")
        threading.Thread(target=handle_client, args=(conn1, addr1, 'X')).start()
        
        conn2, addr2 = s.accept()
        print(f"Conectado com {addr2}")
        threading.Thread(target=handle_client, args=(conn2, addr2, 'O')).start()

if __name__ == "__main__":
    main()
