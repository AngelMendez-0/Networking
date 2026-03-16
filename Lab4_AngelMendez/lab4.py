# Author: Angel Mendez

from sys import argv
from socket import *
from urllib.parse import urlparse

if len(argv) != 4:
    print("Usage: python3 lab4.py [-p|-f] <port> <URL>")
    exit()
    
flag = argv[1]
port = int(argv[2])
url = argv[3]

# parse 
parseUrl = urlparse(url)
host = parseUrl.hostname
path = parseUrl.path

if path == "":
    path = "/"

# GeeksforGeeks Helped with the next 10 lines of code (notated in README)
clientSocket = socket(AF_INET, SOCK_STREAM)
try:
    clientSocket.connect((host, port))
except Exception as e:
    print("Connection error:", e)
    exit()

# step 2: Create TCP
request = "GET " + path + " HTTP/1.0\r\n"
request += "Host: " + host + "\r\n\r\n"

clientSocket.send(request.encode())

# Step 3: get webpage
response = b""
while True:
    data = clientSocket.recv(4096)
    if not data:
        break
    response += data

clientSocket.close()
# Decode
response = response.decode()

#remove header
parts = response.split("\r\n\r\n", 1)
body = parts[1] if len(parts) > 1 else response

# Step 4: output
if flag == "-p":
    print(body, end="")
elif flag == "-f":
    file = open("output.txt", "w")
    file.write(body)
    file.close()

