from _thread import *
import json
import socket
import time

class socketClient():
    
    HOST = '127.0.0.1'
    PORT = 9999
    json_object = {
        "state": 'change',
        "ticker": "BTC",
        "buy_limit": 2000
    }

    def __init__(self):
        super().__init__()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))
        self.alive = True

    def client_run(self):
        start_new_thread(self.recv_data, (self.client_socket,))
        print('>> Connect Server')
        
        while self.alive:
            print('json :',self.json_object)
            json_string = json.dumps(self.json_object)
            self.client_socket.send(json_string.encode())
            time.sleep(10)                       
        self.client_socket.close()

    def recv_data(self,client_socket):
        while True:
            try:
                data = client_socket.recv(1024)
                print("recive : ", repr(data.decode()))
            except ConnectionResetError as ex:
                break
            except Exception as ex:
                print(ex)
        self.alive = False

client = socketClient()
client.client_run()