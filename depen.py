from subprocess import Popen,PIPE,check_output
import os
from colors import *

class Dependecias():
	def __init__(self):		
		self.numeros = 0
		self.VerificarDepen()
		
	def VerificarDepen(self):		
		lib = ["hostapd","dnsmasq","dhcpd","lighttpd","iwconfig","rfkill","xterm","aireplay-ng","airodump-ng"]
		for i in lib:	
			com4 = "if hash %s 2>/dev/null;then echo 'Installed';fi"%i	
			tubo = Popen([com4],shell=True,stdout=PIPE, stderr=PIPE,stdin=PIPE)
			stdout,stderr = tubo.communicate()
			if 'Installed' in str(stdout):
				pass				
				#print G+'[+]'+W+' Installed %s'%i									
			else:			
				print R+'[+]'+W+' Not Install %s'%i
				self.numeros = self.numeros +1				
		if self.numeros >0:
			self.ActualizarDepe()

	def installDepedencias(self):
			lib = ["hostapd","dnsmasq","dhcpd","lighttpd","iwconfig","rfkill","xterm","aireplay-ng","airodump-ng"]
			for i in lib:	
				com4 = "if hash %s 2>/dev/null;then echo 'Installed';fi"%i	
				tubo = Popen([com4],shell=True,stdout=PIPE, stderr=PIPE,stdin=PIPE)
				stdout,stderr = tubo.communicate()
				if 'Installed' in str(stdout):
					print "Installed %s"%i				
				else:
					print R+'[+]'+W+' Not Install %s'%i
					if i == "dhcpd":
						os.system("apt-get --yes --force-yes install isc-dhcp-server")						
					else:
						os.system("apt-get --yes install %s"%i)
						

	def ActualizarDepe(self):
		cmd2 = os.system("echo '# Kali linux repositories | Added by RockWifi\ndeb http://http.kali.org/kali kali-rolling main contrib non-free\ndeb http://repo.kali.org/kali kali-bleeding-edge main' >> /etc/apt/sources.list")
		os.system('apt-get update -m')
		os.system('apt-get install')	
		self.installDepedencias()