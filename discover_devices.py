# discover devices 
# by clach04 (https://github.com/clach04)
# found at https://github.com/codetheweb/tuyapi/issues/5#issuecomment-348799963
# tested with Python 3.6.4 on Gentoo Linux

import socket
import struct


host_port = 6666
host_ip = '239.255.255.250'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
sock.bind(('', host_port))

mreq = struct.pack('4sl', socket.inet_aton(host_ip), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

try:
    while True:
        print('listening')
        data = sock.recvfrom(1024)
        raw_bytes, peer_info = data
        print(data)
finally:
    sock.close()

