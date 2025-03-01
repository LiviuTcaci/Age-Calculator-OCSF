import socket
import threading

class AbstractServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_listening = False
        self.clients = []

    def listen(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
            self.is_listening = True
            print("Serverul este acum în ascultare pe portul", self.port)

            while self.is_listening:
                client_socket, client_address = self.server_socket.accept()
                print("Client conectat:", client_address)

                # Creează un fir nou pentru fiecare client conectat
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()
                self.clients.append((client_socket, client_thread))
        except Exception as e:
            print("Eroare la ascultare:", e)

    def stop_listening(self):
        self.is_listening = False
        for connection in self.clients:
            connection.stop()  # Închide fiecare conexiune activă
        self.server_socket.close()  # Închide socket-ul serverului
        print("Serverul a fost oprit.")

    def send_to_client(self, client_socket, message):
        client_socket.sendall(message.encode())

    def close_client(self, client_socket):
        client_socket.close()
        print("Client deconectat.")