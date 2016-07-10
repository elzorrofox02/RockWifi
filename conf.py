c_PORT_NUMBER = 80
c_ssl_port = 443
c_IP = "192.168.0.1"
c_ips = "192.168.0"
c_DHCP_LEASE = "192.168.0.2,192.168.0.254,12h"
c_RANG_IP = c_ips
#Rutas
c_DUMP_PATH="/tmp/RockWifi"
c_ACTUAL_PATH = os.getcwd()
c_wifiurl = "scan"

#Wifi
c_interface = "wlan0"
c_interairm = False 
c_Host_SSID = "Roque"
c_Host_CHAN = "6"

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