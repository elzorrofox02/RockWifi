try:
	from http.server import HTTPServer,SimpleHTTPRequestHandler,BaseHTTPRequestHandler
except ImportError:
	from BaseHTTPServer import HTTPServer
	from SimpleHTTPServer import SimpleHTTPRequestHandler
	from BaseHTTPServer import BaseHTTPRequestHandler
import threading
import ssl

class ServerSecure(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		HandlerClass = HandlerSecure
		ServerClass = HTTPServer
		self.httpd = ServerClass(('0.0.0.0', 443), HandlerClass)
		self.httpd.socket = ssl.wrap_socket (self.httpd.socket,keyfile="othes/server.pem",certfile='othes/server.pem', server_side=True)

	def run(self):
		print ("Corriendo 443")
		self.httpd.serve_forever()

	def shutdown(self):
		self.httpd.shutdown()
		self.httpd.socket.close()

class HandlerSecure(BaseHTTPRequestHandler):
	def do_GET(self):		
		self.send_response(301)
		#self.send_header('Location', 'http://' + NETWORK_GW_IP + ':' + str(PORT))
		self.send_header('Location', 'http://127.0.0.1')
		self.end_headers()	

	def log_message(self, format, *args):
		return

class ServerHttpd(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		HandlerClass = HandlerHttpd
		ServerClass = HTTPServer
		self.httpd = ServerClass(('0.0.0.0', 80), HandlerClass)

	def run(self):
		print ("Corriendo 80")
		self.httpd.serve_forever()

	def shutdown(self):
		self.httpd.shutdown()
		self.httpd.socket.close()

class HandlerHttpd(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/plain")
		self.end_headers()
		message = "Hello world 80!"
		self.wfile.write(bytes(message, "utf8"))

	def log_message(self, format, *args):
		return

hola = ServerSecure()
hola.start()

hola2 = ServerHttpd()
hola2.start()

xd = input("ingrea :: ")
if xd == "1":
	hola.shutdown()
	hola2.shutdown()




