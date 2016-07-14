"""
from http.server import HTTPServer,SimpleHTTPRequestHandler,BaseHTTPRequestHandler
from socketserver import BaseServer
import ssl
import socket
from threading import Thread, Lock



NETWORK_GW_IP = "127.0.0.1"
PORT = 80
xd = 'Location', 'http://www.gooogle.co.ve'

class SecureHTTPServer(HTTPServer):
	def __init__(self, server_address, HandlerClass):
		BaseServer.__init__(self, server_address, HandlerClass)		
		ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
		ctx.load_cert_chain(certfile="server.pem", keyfile="server.pem")
		self.socket = ctx.wrap_socket(socket.socket(self.address_family, self.socket_type), server_side=True)
		self.server_bind()
		self.server_activate()


	def serve_forever(self):		    
		self.stop = False
		while not self.stop:
			self.handle_request()

class SecureHTTPRequestHandler(BaseHTTPRequestHandler):	
	#def do_QUIT(self):    
	#	self.send_response(200)
	#	self.end_headers()
	#	self.server.stop = True

	#def setup(self):
		#self.connection = self.request
		#self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
		#self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)

	def do_GET(self):
		print ("Get")
		self.send_response(301)
		#self.send_header('Location', 'http://' + NETWORK_GW_IP + ':' + str(PORT))
		self.send_header('Location', 'http://www.google.co.ve')
		self.end_headers()
		
		#self.send_response(200)	
		#self.send_header('Content-type','text/html')
		#self.end_headers()	
		#message = "Hello world!"		
		#self.wfile.write(bytes(message, "utf8"))

	def log_message(self, format, *args):
		return



httpd = SecureHTTPServer(("", 443), SecureHTTPRequestHandler)
httpd.serve_forever()
"""
"""


from http.server import HTTPServer,SimpleHTTPRequestHandler,BaseHTTPRequestHandler
from socketserver import BaseServer
import ssl
from threading import Thread, Lock
from socketserver import ThreadingMixIn
import sys, os, socket



class SecureHttpdHandler(BaseHTTPRequestHandler):
	print ("hjand")
	def do_GET(self):
		self.send_response(200)	
		self.send_header('Content-type','text/html')
		self.end_headers()	
		message = "Hello world!"		
		self.wfile.write(bytes(message, "utf8"))	
		return


def run():
	try:
		httpd = HTTPServer(('localhost', 443), SecureHttpdHandler)
		httpd.socket = ssl.wrap_socket (httpd.socket, certfile='server.pem', server_side=True)
		#httpd.socket = ssl.wrap_socket (httpd.socket,keyfile="server.pem",certfile='server.pem', server_side=True)
		print ("corriendo")
		secure_webserver = Thread(target=httpd.serve_forever)
		secure_webserver.daemon = True
		secure_webserver.start()	
		#httpd.serve_forever()
	except KeyboardInterrupt:
		print ('^C received, shutting down the web server')
		httpd.socket.close()
	

if __name__ == "__main__":
	run()
"""

#try:
#	from http.server import HTTPServer as http_server
#except ImportError:
#	from SocketServer import TCPServer as http_server
#try:
#	from http.server import SimpleHTTPRequestHandler \
#		as http_handler
#except ImportError:
#	from SimpleHTTPServer import SimpleHTTPRequestHandler \
#		as http_handler

"""
import threading

from http.server import HTTPServer,SimpleHTTPRequestHandler,BaseHTTPRequestHandler

from threading import Thread
from socketserver import ThreadingMixIn
import cgi,os,sys,time
#from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/plain")
		self.end_headers()
		message = "Hello world!"
		self.wfile.write(bytes(message, "utf8"))
		self.server_close()

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
	pass

def serve_on_port(port):
	server = ThreadingHTTPServer(("localhost",port), Handler)
	server.serve_forever()

hola = Thread(target=serve_on_port, args=[1111]).start()
print ("chavez vive")

xd = input("ingrea :: ")
if xd == "1":
	#hola.wait()
	sys.exit()
#serve_on_port(2222)
#falta detenerlo
"""
"""
import http.server
from http.server import HTTPServer,SimpleHTTPRequestHandler,BaseHTTPRequestHandler
import threading
import sys



import ssl
from socketserver import ThreadingMixIn



class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/plain")
		self.end_headers()
		message = "Hello world!"
		self.wfile.write(bytes(message, "utf8"))	


	def log_message(self, format, *args):
		return


class StoppableHTTPServer(HTTPServer):
	def run(self):
		try:
			#Forma 1

			#self.socket = ssl.wrap_socket (self.socket, certfile='server.pem', server_side=True)
			#ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
			#ctx.load_cert_chain(certfile="server.pem", keyfile="server.pem")
			#self.socket = ctx.wrap_socket(socket.socket(self.address_family, self.socket_type), server_side=True)
			#self.server_bind()
			#self.server_activate()
			#self.serve_forever()

			#OR Forma 2

			self.socket = ssl.wrap_socket (self.socket,keyfile="server.pem",certfile='server.pem', server_side=True)
			self.serve_forever()
		except KeyboardInterrupt:
			pass
		finally:
			self.server_close()


server = StoppableHTTPServer(("127.0.0.1", 443),Handler)
thread = threading.Thread(None, server.run)
thread.start()

xd = input("ingrea :: ")
if xd == "1":	
	server.shutdown()
	thread.join()
else:
	server.shutdown()
	thread.join()
	sys.exit()

"""
try:
    from http.server import HTTPServer as http_server
except ImportError:
    from SocketServer import TCPServer as http_server
try:
    from http.server import SimpleHTTPRequestHandler \
        as http_handler
except ImportError:
    from SimpleHTTPServer import SimpleHTTPRequestHandler \
        as http_handler

from http.server import HTTPServer,SimpleHTTPRequestHandler,BaseHTTPRequestHandler
import threading
import ssl

class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/plain")
		self.end_headers()
		message = "Hello world!"
		self.wfile.write(bytes(message, "utf8"))	


	def log_message(self, format, *args):
		return




class Server(threading.Thread):
	def __init__(self, port, address):
		threading.Thread.__init__(self)
		HandlerClass = Handler
		ServerClass = http_server
		self.httpd = ServerClass(('127.0.0.1', 443), HandlerClass)
		self.httpd.socket = ssl.wrap_socket (self.httpd.socket,keyfile="server.pem",certfile='server.pem', server_side=True)

	def run(self):
		self.httpd.serve_forever()

	def shutdown(self):
		self.httpd.shutdown()
		self.httpd.socket.close()


hola = Server(80,"127.0.0.1")
hola.start()

xd = input("ingrea :: ")
if xd == "1":
	hola.shutdown()



"""
import threading
try: 
  from http.server import HTTPServer, BaseHTTPRequestHandler # Python 3
except ImportError: 
  import SimpleHTTPServer
  from BaseHTTPServer import HTTPServer # Python 2
  from SimpleHTTPServer import SimpleHTTPRequestHandler as BaseHTTPRequestHandler


server = HTTPServer(('localhost', 0), BaseHTTPRequestHandler)
thread = threading.Thread(target = server.serve_forever)
thread.deamon = True
def up():
  thread.start()
  print('starting server on port {}'.format(server.server_port))
def down():
  server.shutdown()
  print('stopping server on port {}'.format(server.server_port))



"""