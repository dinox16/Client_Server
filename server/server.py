# -*- coding: utf-8 -*-
"""
Server chat - Chat Server
Quan ly ket noi tu nhieu client va relay tin nhan da ma hoa
"""

import socket
import threading
import json


class ChatServer:
    """
    Server chat hub
    - Lang nghe ket noi tu clients
    - Quan ly danh sach clients
    - Relay tin nhan ma hoa giua cac clients
    """
    
    def __init__(self, host='0.0.0.0', port=5555):
        """
        Khoi tao server
        
        Args:
            host: Dia chi IP lang nghe (mac dinh 0.0.0.0)
            port: Cong lang nghe (mac dinh 5555)
        """
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = {}  # {socket: {'username': name, 'public_key': key}}
        self.lock = threading.Lock()
    
    def start(self):
        """Khoi dong server va lang nghe ket noi"""
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"[SERVER] Dang lang nghe tai {self.host}:{self.port}")
            
            while True:
                client_socket, address = self.server_socket.accept()
                print(f"[SERVER] Ket noi moi tu {address}")
                
                # Tao thread xu ly client
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket,)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\n[SERVER] Dang dong server...")
            self.shutdown()
        except Exception as e:
            print(f"[ERROR] Loi server: {e}")
            self.shutdown()
    
    def handle_client(self, client_socket):
        """
        Xu ly client connection
        
        Args:
            client_socket: Socket cua client
        """
        try:
            # Nhan thong tin dang ky (username + public key)
            registration_data = client_socket.recv(8192).decode('utf-8')
            registration = json.loads(registration_data)
            
            username = registration['username']
            public_key = registration['public_key']
            
            # Luu thong tin client
            with self.lock:
                self.clients[client_socket] = {
                    'username': username,
                    'public_key': public_key
                }
            
            print(f"[SERVER] {username} da dang ky thanh cong")
            
            # Broadcast danh sach users
            self.broadcast_user_list()
            
            # Nhan va relay tin nhan
            while True:
                data = client_socket.recv(8192).decode('utf-8')
                if not data:
                    break
                
                try:
                    message_packet = json.loads(data)
                    self.relay_message(client_socket, message_packet)
                except json.JSONDecodeError:
                    print(f"[ERROR] Nhan duoc du lieu khong hop le tu {username}")
                
        except Exception as e:
            print(f"[ERROR] Loi xu ly client: {e}")
        finally:
            # Xoa client va dong ket noi
            with self.lock:
                if client_socket in self.clients:
                    username = self.clients[client_socket]['username']
                    del self.clients[client_socket]
                    print(f"[SERVER] {username} da ngat ket noi")
            
            try:
                client_socket.close()
            except:
                pass
            
            # Broadcast lai danh sach users
            self.broadcast_user_list()
    
    def relay_message(self, sender_socket, message_packet):
        """
        Chuyen tiep tin nhan da ma hoa den nguoi nhan
        
        Args:
            sender_socket: Socket cua nguoi gui
            message_packet: Goi tin da ma hoa
        """
        try:
            sender_username = self.clients[sender_socket]['username']
            recipient_username = message_packet['to']
            
            print(f"[SERVER] Relay tin nhan tu {sender_username} den {recipient_username}")
            
            # Tim socket cua nguoi nhan
            recipient_socket = None
            with self.lock:
                for sock, info in self.clients.items():
                    if info['username'] == recipient_username:
                        recipient_socket = sock
                        break
            
            if recipient_socket:
                # Gui tin nhan da ma hoa (khong decrypt)
                message_data = json.dumps(message_packet)
                recipient_socket.send(message_data.encode('utf-8'))
                print(f"[SERVER] Da gui tin nhan den {recipient_username}")
            else:
                print(f"[WARNING] Khong tim thay {recipient_username}")
                
        except Exception as e:
            print(f"[ERROR] Loi relay tin nhan: {e}")
    
    def broadcast_user_list(self):
        """Gui danh sach users va public keys cho tat ca clients"""
        try:
            with self.lock:
                user_list = {}
                for sock, info in self.clients.items():
                    user_list[info['username']] = info['public_key']
            
            broadcast_packet = {
                'type': 'user_list',
                'users': user_list
            }
            
            broadcast_data = json.dumps(broadcast_packet)
            
            # Gui cho tat ca clients
            with self.lock:
                disconnected = []
                for sock in self.clients.keys():
                    try:
                        sock.send(broadcast_data.encode('utf-8'))
                    except:
                        disconnected.append(sock)
                
                # Xoa cac ket noi bi loi
                for sock in disconnected:
                    if sock in self.clients:
                        del self.clients[sock]
            
            print(f"[SERVER] Da broadcast danh sach {len(user_list)} users")
            
        except Exception as e:
            print(f"[ERROR] Loi broadcast user list: {e}")
    
    def shutdown(self):
        """Dong server"""
        print("[SERVER] Dang dong tat ca ket noi...")
        with self.lock:
            for sock in self.clients.keys():
                try:
                    sock.close()
                except:
                    pass
        try:
            self.server_socket.close()
        except:
            pass
        print("[SERVER] Da dong server")


def main():
    """Ham main chay server"""
    print("="*60)
    print("CHAT SERVER - Mang May Tinh")
    print("="*60)
    
    server = ChatServer(host='0.0.0.0', port=5555)
    server.start()


if __name__ == '__main__':
    main()
