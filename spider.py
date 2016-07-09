import csv

wifi = "datos.cap-01.csv"
wifi2 = "jr.cap-01.csv"
prueba = "prov.csv"


class ListaAp():
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




hola = ListaAp(wifi2)
hola.BorrarPrimera()
hola.Leer()