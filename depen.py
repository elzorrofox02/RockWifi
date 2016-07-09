from subprocess import Popen,PIPE,check_output
import subprocess
import os

#com = 'dpkg -l | grep hostapd'
#com2 = 'dpkg --get-selections | grep lighttpd'

"""
hola = ["hostapd","lighttpd","iwconfig","rfkill","XTerm","aireplay-ng","airodump-ng"]

for i in hola:	
	com2 = 'dpkg --get-selections | grep %s'%i	
	hola = Popen([com2],shell=True,stdout=PIPE, stderr=PIPE,stdin=PIPE)
	stdout,stderr = hola.communicate()
	if 'install' in str(stdout):
		print "instaldo %s"%i
	else:
		print "NOOOOOOOOOOOO %s"%i
		#os.system("apt-get --yes install %s"%i)
	#print stdout
"""
com4 = "if hash iwconfig 2>/dev/null;then echo 'Installed';fi"
hola = Popen([com4],shell=True,stdout=PIPE, stderr=PIPE,stdin=PIPE)
stdout,stderr = hola.communicate()
if 'Installed' in str(stdout):
	print "Installed "
else:
	print "NOt Install"
#print stdout


#os.system("if hash iwconfig 2>/dev/null;then echo 'Ok';fi")
	
"""
com3 = 'dpkg --get-selections | grep dhcpd'
hola = Popen([com3],shell=True,stdout=PIPE, stderr=PIPE,stdin=PIPE)
stdout,stderr = hola.communicate()
if 'install' in str(stdout):
	print "instaldo"
else:
	print "NOOOOOOOOOOOO"
	os.system("apt-get --yes install isc-dhcp-server --force-yes")
print stdout
"""