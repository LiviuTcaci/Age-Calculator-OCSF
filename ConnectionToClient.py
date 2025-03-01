import threading

class ConnectionToClient(threading.Thread):
    def __init__(self, client_socket, client_address, server):
        super().__init__()
        self.client_socket = client_socket
        self.client_address = client_address
        self.server = server
        self.running = True

    def run(self):
        try:
            while self.running:
                message = self.client_socket.recv(1024).decode()
                if message:
                    print(f"Mesaj de la {self.client_address}: {message}")
                    self.server.handle_message_from_client(self, message)
                else:
                    self.stop()
        except Exception as e:
            print("Eroare în conexiunea cu clientul:", e)
        finally:
            self.stop()

    def send_to_client(self, message):
        try:
            self.client_socket.sendall(message.encode())
        except Exception as e:
            print(f"Eroare la trimiterea mesajului către {self.client_address}:", e)
            self.stop()

    def stop(self):
        """Închide conexiunea cu clientul."""
        if self.running:
            self.running = False
            try:
                self.client_socket.close()
            except Exception as e:
                print(f"Eroare la închiderea conexiunii cu clientul {self.client_address}: {e}")
            print(f"Client deconectat: {self.client_address}")
            # Eliminăm clientul din lista serverului
            if self in self.server.clients:
                self.server.clients.remove(self)
