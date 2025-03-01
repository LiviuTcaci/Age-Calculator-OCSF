from datetime import datetime
from AbstractClient import AbstractClient
import sys

class ConcreteClient(AbstractClient):
    def open_connection(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print("Conexiune stabilită cu serverul.")
        except ConnectionRefusedError:
            print(
                "Eroare: Serverul nu este pornit sau nu poate fi accesat. Verificați conexiunea și încercați din nou.")
            sys.exit(1)  # Oprește aplicația dacă serverul nu este pornit
        except Exception as e:
            print("Eroare la conectarea cu serverul:", e)
            sys.exit(1)

    def validate_birth_date(self, birth_date_str):
        try:
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
            today = datetime.today()

            if birth_date > today:
                print("Eroare: Data de naștere nu poate fi în viitor.")
                return False
            return True
        except ValueError:
            print("Eroare: Formatul datei de naștere este invalid. Folosiți formatul YYYY-MM-DD.")
            return False

    def main(self):
        # Deschide conexiunea
        self.open_connection()

        while True:
            birth_date = input("Introduceți data de naștere (format YYYY-MM-DD): ")
            if self.validate_birth_date(birth_date):
                print("Data validă. Se trimite cererea către server...")
                break

        # Trimite data de naștere către server
        self.send_to_server(birth_date)

        # Primește și afișează răspunsul de la server
        response = self.receive_from_server()
        if response:
            print("Răspunsul serverului:", response)

        # Închide conexiunea
        self.close_connection()


# Pornirea aplicației client
if __name__ == "__main__":
    client = ConcreteClient()
    client.main()