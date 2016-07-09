class Interfaces():
	def iwconfig():
		monitors = []
		interfaces = {}
		proc = Popen(['iwconfig'], stdout=PIPE, stderr=DN)
		for line in proc.communicate()[0].split('\n'):
			if len(line) == 0: continue # Isn't an empty string
			if line[0] != ' ': # Doesn't start with space
				#ignore_iface = re.search('eth[0-9]|em[0-9]|p[1-9]p[1-9]|at[0-9]', line)
				#if not ignore_iface: # Isn't wired or at0 tunnel
				iface = line[:line.find(' ')] # is the interface name
				if 'Mode:Monitor' in line:
					monitors.append(iface)
				elif 'IEEE 802.11' in line:
					if "ESSID:\"" in line:
						interfaces[iface] = 1
					else:
						interfaces[iface] = 0
		return monitors, interfaces
interfaces().iwconfig()