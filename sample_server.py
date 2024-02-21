import socket as s
from threading import Thread
import mimetypes as m

http_resp_template = """HTTP/1.1 200 OK
Connection: Keep-Alive
Content-Type: {type}
Accept-Ranges: bytes
Content-Length: {length}
Vary: Accept-Encoding
Server: Apache/2.4.41 (Ubuntu)

{body}"""

htdocs = 'htdocs'

HOST = '0.0.0.0' #configure port forwarding to get internet traffic
PORT = 3074

class ASPIncomingThread(Thread):
	def __init__(self, conn, addr):
		Thread.__init__(self)
		self.conn = conn
		self.addr = addr
		print("Thread {}:{} started...".format(addr[0], addr[1]))
	
	def run(self):
		data = conn.recv(4096)
		rl = data.decode().split('\n')[0]
		print(rl)
		f = rl.split(' ')[1]
		if f == "/":
			f = "index.html"
		f = 'htdocs/'+f
		with open(f, 'r') as file:
			body = file.read()
		self.conn.sendall(http_resp_template.format(type=m.guess_type(f)[0], length=len(body), body=body).encode())
#		data = conn.recv(4096)
#		while data:
#			print("{}: ".format(self.addr[0]) + data.decode(), end="")
#			data = conn.recv(1024)

sck = s.socket(s.AF_INET, s.SOCK_STREAM)
sck.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
sck.bind((HOST, PORT))
sck.listen()
while True:
	print("Waiting for a new connection...")
	conn, addr = sck.accept()
	print("Connection received from {}:{}".format(addr[0], addr[1]))
	ASPIncomingThread(conn, addr).start()
	