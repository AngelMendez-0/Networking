Author: Angel Mendez

How to run: 

python3 lab4.py [-p|-f] <port> <URL>


Questions: 

1. Why did you have to encode() your request and decode() the response(s)? What do these functions do?

Answer: encode converts python strings to bytes for easy transportation whilst decode converts them back into strings for easy reading

2. What changes would you have to make to create a UDP socket?

Answer: use sock_dgram instead of sock_stream, I'd also have to not call connect and instead use sendto()/recvfrom

3. If you wanted to create a TCP server, what would you have to change?

Answer: I'd have to use bind to a port and listen to wait for the response as well as accept() the sockets using recv() and send()

4. Can your TCP client create or process HTTPS traffic? What happens ifyou send a request to port 443?

Answer: this doesn't support HTTP and if you used port 443 it would fail or spit out data that wouldn't be readable

Citations: 

https://realpython.com/python-sockets/

https://www.geeksforgeeks.org/socket-programming-python/
