import socket
import struct

UDP_IP = '127.0.0.1'
UDP_PORT = 7777

data = (100,1)
packed_data = bytes()
packed_data = packed_data.join((struct.pack('B',val) for val in data))

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.sendto(packed_data,(UDP_IP,UDP_PORT))
