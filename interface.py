from subprocess import Popen,PIPE
import os

class Interfaces():
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
					monitors.append(iface)
				elif 'IEEE 802.11' in line:										
					numer = num+1
					interfaces[numer] = iface
						
		
		for clave,valor in interfaces.items():
			print "%s) %s"%(clave,valor)			
		elige1 = raw_input(" Elige Interface > ")
		seleccion = interfaces.get(int(elige1))

		print "Haz Selecionado %s"%seleccion


		return monitors, interfaces
Interfaces().iwconfig()