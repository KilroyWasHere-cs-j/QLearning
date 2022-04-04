import socket


class sender:

    def __init__(self):
        self.handshake = 5687
        self.handshook_code = 1111
        self.handshook = False

    def handShake(self):
        self.send(self.handshake)

    def send(self, msg):
        UDP_IP_ADDRESS = "127.0.0.1"
        UDP_PORT_NO = 6789
        Message = bytes(str(msg), 'utf-8')

        clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        clientSock.sendto(Message, (UDP_IP_ADDRESS, UDP_PORT_NO))



