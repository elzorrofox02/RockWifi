from subprocess import Popen,PIPE
import os,sys
from conf import *
import conf

class Interfaces():
	def __init__(self):
		self.inter = False

	def resul(self):
		return self.inter

	def iwconfig(self):		
		monitors = []
		interfaces = {}
		num = 0
		proc = Popen(['iwconfig'], stdout=PIPE, stderr=PIPE)
		for line in proc.communicate()[0].split('\n'):
			if len(line) == 0: continue # Isn't an empty string
			if line[0] != ' ': # Doesn't start with space				
				iface = line[:line.find(' ')] # is the interface name
				if 'Mode:Monitor' in line:
					conf.c_interairm = iface
					numer = num+1					
					monitors.append(iface)
					interfaces[numer] = iface
				elif 'IEEE 802.11' in line:										
					numer = num+1
					interfaces[numer] = iface					
		
		for clave,valor in interfaces.items():
			print G+"%s) %s %s"%(clave,W,valor)			 
		try:
			elige1 = raw_input("Elige Interface: ")
			if elige1.isdigit():
				seleccion = interfaces.get(int(elige1))
				if seleccion == None:
					print "No Valido Seleccione Una Interface Valida"
					self.iwconfig()
				else:
					print "Haz Selecionado %s"%seleccion
			else:
				print "Comando Invalido"
				sys.exit()			

			self.inter = seleccion
			conf.c_ActualInterface = self.inter
		except KeyboardInterrupt:
			sys.exit()		
		return self.inter