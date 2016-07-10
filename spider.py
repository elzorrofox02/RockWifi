import csv
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR) #eleimiar error scapy ipv6
from scapy.all import *

wifi = "datos.cap-01.csv"
wifi2 = "jr.cap-01.csv"
prueba = "prov.csv"
ap_list = []
Aps = {}
count = 0

class ListaApAir():
	def __init__(self,url):
		self.url = url		
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

class ListaApAir():
	def __init__(self,iface):
		sniff(iface=iface, prn = self.PacketHandler)
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
	def resultado():
		print resultado
		return resultado

hola = raw_input("Selecciona:")
if hola == "1":	
	ListaApAir("wlan0mon")
if hola == "2":
	resultado

"""
hola = ListaAp(wifi2)
hola.BorrarPrimera()
hola.Leer()
"""
