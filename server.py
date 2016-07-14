from http.server import HTTPServer,SimpleHTTPRequestHandler,BaseHTTPRequestHandler
import threading
import ssl

class HandlerSecure(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/plain")
		self.end_headers()
		message = "Hello world!"
		self.wfile.write(bytes(message, "utf8"))	


	def log_message(self, format, *args):
		return

class ServerSecure(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		HandlerClass = HandlerSecure
		ServerClass = HTTPServer
		self.httpd = ServerClass(('127.0.0.1', 443), HandlerClass)
		self.httpd.socket = ssl.wrap_socket (self.httpd.socket,keyfile="server.pem",certfile='server.pem', server_side=True)

		#Forma 1
		#self.socket = ssl.wrap_socket (self.socket, certfile='server.pem', server_side=True)
		#ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
		#ctx.load_cert_chain(certfile="server.pem", keyfile="server.pem")
		#self.socket = ctx.wrap_socket(socket.socket(self.address_family, self.socket_type), server_side=True)
		#self.server_bind()
		#self.server_activate()

	def run(self):
		self.httpd.serve_forever()

	def shutdown(self):
		self.httpd.shutdown()
		self.httpd.socket.close()


hola = ServerSecure()
hola.start()

xd = input("ingrea :: ")
if xd == "1":
	hola.shutdown()



