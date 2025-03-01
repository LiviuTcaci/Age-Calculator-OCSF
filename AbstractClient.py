import socket

class AbstractClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def open_connection(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print("Conexiune stabilită cu serverul.")
        except Exception as e:
            print("Eroare la conectarea cu serverul:", e)

    def send_to_server(self, message):
        try:
            self.client_socket.sendall(message.encode())
        except Exception as e:
            print("Eroare la trimiterea mesajului:", e)

    def receive_from_server(self):
        try:
            response = self.client_socket.recv(1024).decode()
            return response
        except Exception as e:
            print("Eroare la primirea răspunsului:", e)
            return None

    def close_connection(self):
        self.client_socket.close()
        print("Conexiune închisă.")