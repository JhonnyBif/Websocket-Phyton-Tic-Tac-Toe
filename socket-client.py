import socket

# Configurações do servidor
HOST = '' #YOUR IP  
PORT = 0000 ## YOUR PORT  

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        
        while True:
            data = s.recv(1024).decode()
            if not data:
                break
            print(data)
            
            if "O jogo acabou!" in data or "venceu!" in data or "Empate!" in data:
                replay = input("Deseja jogar novamente? (digite 'replay'): ")
                s.sendall(replay.encode())
            elif "Sua vez de jogar" in data:
                move = input("Digite sua jogada (linha,coluna): ")
                s.sendall(move.encode())

if __name__ == "__main__":
    main()
