import csv,sys
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR) #eleimiar error scapy ipv6
from scapy.all import *
from threading import Thread, Lock
import conf
ap_list = []
Aps = {}
count = 0

class ListaApAir():
	def __init__(self,url):
		self.url = url	

	def Scan(self):
		os.system('airmon-ng start %s'%c_interface)
		os.system('xterm -title "Escaneando Objetivos ..." -bg "#FFFFFF" -fg "#000000" -e airodump-ng -w %s/%s -a mon0'%(c_DUMP_PATH,c_wifiurl))	
	def Leer(self):
		with open(self.url) as csvfile:
			reader = csv.DictReader(csvfile,skipinitialspace=True,strict=True)	
			for row in reader:				
				if row['BSSID'] == "Station MAC":
					break
				print(row['BSSID'], row['Power'], row['Privacy'],row['channel'],row['ESSID'])

	def BorrarPrimera(self):
		# abrimos el archivo solo de lectura
		f = open(self.url,"r") 
		lineas = f.readlines()
		f.close()		 
		# abrimos el archivo pero vacio
		f = open(self.url,"w") 
		for linea in lineas:    
			if linea!="\n": 
				# Si no es la linea que queremos eliminar, guardamos la linea en el archivo
				f.write(linea)
		f.close()

"""
hola = ListaAp(wifi2)
hola.BorrarPrimera()
hola.Leer()
"""
class ListaApAir2():
	def __init__(self,iface):
		chanhop = Thread(target=self.canalC, args=(iface,))
		chanhop.daemon = True
		chanhop.start()
		sniff(iface=iface, prn=self.PacketHandler)		

	def canalC(self,iface):
	canal = 0
	while conf.c_canal_daemon_corriendo:
		try:
			if canal > 11:
				canal = 0
			canal = canal + 1
			channel = str(canal)
			print (channel)            
			iw = Popen(['iw', 'dev', iface, 'set', 'channel', channel],stdout=DN, stderr=PIPE)
			for line in iw.communicate()[1].split('\n'):               
				if len(line) > 2:
					with lock:
						err = (
							'[' + R + '-' + W + '] Channel hopping failed: ' +
							R + line + W + '\n'
							'Try disconnecting the monitor mode\'s parent' +
							'interface (e.g. wlan0)\n'
							'from the network if you have not already\n'
						)
						sys.exit(err)
					break            
			time.sleep(1)
		except KeyboardInterrupt:
			sys.exit()

	def PacketHandler(self,pkt):
		global Aps,count
		if pkt.haslayer(Dot11):
			if pkt.type == 0 and pkt.subtype == 8:						
				if pkt.addr2 not in ap_list :					
					ap_list.append(pkt.addr2)
					mac = pkt.addr2
					ssid = pkt.info
					canal = str(ord(pkt[Dot11Elt:3].info)) #canal
					senal = -(256 - ord(pkt.notdecoded[-2:-1]))	
					print "%s %s %s Signal : %s " %(mac, canal,ssid,senal)
					count += 1
					Aps[count] = [canal,ssid,mac]					
	def resultado(self):
		return Aps		


ListaApAir2()