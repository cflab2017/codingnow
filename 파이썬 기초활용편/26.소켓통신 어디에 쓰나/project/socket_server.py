import socket
from _thread import *
import json

class socketServer():
    client_sockets = [] #클라이언트 목록
    HOST = '127.0.0.1'
    PORT = 9999

    def __init__(self):
        print('>> Server Start')
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen()

    def server_run(self):
        try:
            while True:
                print('>> Wait')
                client_socket, addr = self.server_socket.accept()
                self.client_sockets.append(client_socket)
                start_new_thread(self.thread_client, (client_socket, addr))
                print("연결된 수 : ", len(self.client_sockets))
        except Exception as e:
            print('socketServer error : ', e)
        finally:
            self.server_socket.close()            

    def thread_client(self,client_socket, addr):
        print('>> Connected by :', addr[0], ':', addr[1])
        while True:
            data = client_socket.recv(1024*10)
            if not data:
                print('>> Disconnected by ' + addr[0], ':', addr[1])
                break
            print('>> Received from ' + addr[0], ':', addr[1])
            client_socket.send(data)#echo to client
            try:
                json_string = data.decode()
                json_string = json.loads(json_string)
                # print(json_string['state'])
                print(json_string)
            except Exception as ex:
                print('socketServer json.loads :', ex)
                continue

server = socketServer()
server.server_run()