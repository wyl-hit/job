import socket  # for sockets
import sys  # for exit
import struct

# create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

print 'Socket Created'

host = '172.31.137.50'
port = 23460

try:
    remote_ip = socket.gethostbyname(host)

except socket.gaierror:
    # could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()

# Connect to remote server
s.connect((remote_ip, port))

print 'Socket Connected to ' + host + ' on ip ' + remote_ip

# Send some data to remote server
message = "qs177"
try:
    # Set the whole string
    s.send(message)
except socket.error:
    # Send failed
    print 'Send failed'
    sys.exit()

print 'Message send successfully'

# Now receive data
reply = s.recv(4096)

print reply + '1111'
