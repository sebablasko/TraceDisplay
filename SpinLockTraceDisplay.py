import sys
filename = sys.argv[1]

#Generals

#targetFunctions: obtained from /sys/kernel/debug/tracing/available_filter_functions related to *spin* filters
targetFunctions = ["mutex_spin_on_owner","spin_msec","_spin_trylock","_spin_lock_irqsave","_spin_lock_irq","_spin_lock","_spin_unlock_irqrestore","_spin_lock_bh","_spin_trylock_bh","_spin_unlock_bh","bit_spin_lock","kvm_vcpu_on_spin"]
colors = ["brown","black","orange","yellow","purple","green","blue","red","cyan","gray","pink","magenta"]
data = []
appearedFunctions = {}
cpus = {}
anchoVentana = 1320
altoVentana = 700

#tiempos
tiempoInicio = -1
tiempoFin = -1

#dimensiones generales
	#head
altoHead = 50
inicioLinea = 80
finLinea = 1250
	#carriles
altoCarriles = 550

def sumaDuraciones(l):
	return reduce(lambda q,p: float(p)+float(q), l)
def color(funName):
	return colors[targetFunctions.index(funName)]
class Cambio:
	def __init__(self, time, cpu):
		self.cpu = cpu
		self.time = time
	def dibujar(self, lienzo):
	 x = getXbyTime(self.time)
	 y1 = altoHead
	 y2 = altoHead + altoPorCarril*len(appearedFunctions)
	 lienzo.create_line(x, y1, x, y2, )
class Registro:
	def __init__(self, function, cpu, time, duration):
		self.function = function
		self.cpu = cpu
		self.time = time
		self.duration = duration
	def dibujar(self, lienzo):
		y = altoHead + altoPorCarril*cpus.keys().index(self.cpu) + altoPorCarril/(len(appearedFunctions)*2) + appearedFunctions.keys().index(self.function)*altoPorCarril/len(appearedFunctions) +1
		x1 = getXbyTime(self.time)
		x2 = getXbyTime(self.time+self.duration*10**-6)
		if(x1>=inicioLinea and x2<=finLinea):
			lienzo.create_line(x1, y, x2, y, width=(altoPorCarril/len(appearedFunctions)-1), fill=color(self.function))
def obtenerTiempo(linea):
	return linea.split("|")[0].strip()
def obtenerCPU(linea):
	return linea.split("|")[1].split(")")[0].strip()
def obtenerDuracion(linea):
	if "+" in linea:
		return linea.split("|")[2].strip().split("+")[1].strip().split(" ")[0]
	if "!" in linea:
		return linea.split("|")[2].strip().split("!")[1].strip().split(" ")[0]
	return linea.split("|")[2].strip().split(" ")[0]
def obtenerNombre(linea):
	return linea.split("|")[3].strip().split("();")[0]
def getXbyTime(time):
		return inicioLinea+(finLinea-inicioLinea)*(time-tiempoInicio)/(tiempoFin-tiempoInicio)

#Preprocesar los datos
archivo = open(filename, 'r')
for line in archivo:
	if (len(line.split("|")) > 1 and len(line.split("|")) < 6):
		nombre = obtenerNombre(line)
		if nombre in targetFunctions:
			cpu = int(obtenerCPU(line))
			duracion = float(obtenerDuracion(line))
			time = float(obtenerTiempo(line))
			#dibujarLinea(time, duracion*10**-6, cpu, nombre)	
			data.append(Registro(nombre, cpu, time, duracion))
			cpus[cpu] = "1"
			if nombre in appearedFunctions:
				appearedFunctions[nombre].append(duracion)
			else:
				appearedFunctions[nombre] = [duracion]
			if(tiempoInicio == -1):
				tiempoInicio = time
			if(tiempoFin < time):
				tiempoFin = time
	if "=>" in line:
		None


#canvas
from Tkinter import *
ventana = Tk()
ventana.title("SpinLock Function Tracer")
lienzo = Canvas(ventana, width=anchoVentana, height=altoVentana, bg='white')
lienzo.pack()
#head
lienzo.create_text(anchoVentana/2, altoHead/2, text="SpinLock Function Tracer",font=("Arial",20))
lienzo.create_line(inicioLinea, altoHead, finLinea, altoHead, width=1)

#carriles
altoPorCarril = altoCarriles/len(cpus)
indice = 0
for i in cpus:
	title = "CPU#"+str(i)
	alturaTexto = altoHead + altoPorCarril*indice + altoPorCarril/2
	lienzo.create_text(inicioLinea-30, alturaTexto, text=title)
	alturaFinal = altoHead + altoPorCarril*(indice+1)
	lienzo.create_line(inicioLinea, alturaFinal, finLinea, alturaFinal, width=1)
	indice = indice + 1

#linea de tiempo
yLineaTiempo = altoHead + altoCarriles + 25
lienzo.create_line(inicioLinea-10, yLineaTiempo, finLinea+10, yLineaTiempo, width=3)
#rotular
lienzo.create_line(inicioLinea, yLineaTiempo, inicioLinea, yLineaTiempo+10, width=2)
lienzo.create_text(inicioLinea, yLineaTiempo + 20, text=str(tiempoInicio))
lienzo.create_line(finLinea, yLineaTiempo, finLinea, yLineaTiempo+10, width=2)
lienzo.create_text(finLinea, yLineaTiempo + 20, text=str(tiempoFin))
lienzo.create_text(finLinea/2, yLineaTiempo + 10, text="Time [s]", font=("arial",11))

#dibujar registros
for reg in data:
	reg.dibujar(lienzo)

#leyenda
yLeyenda = yLineaTiempo + 30
xLeyenda = inicioLinea + 150
deltaX = 150
for val in appearedFunctions:
	lienzo.create_line(xLeyenda, yLeyenda, xLeyenda+15, yLeyenda, width=8, fill=color(val))
	lienzo.create_text(xLeyenda, yLeyenda + 10, text=val, fill=color(val))
	duracionTotal = sumaDuraciones(appearedFunctions[val])
	lienzo.create_text(xLeyenda, yLeyenda + 22, text=str(duracionTotal)+" [us]", fill=color(val), font=("Arial",9))
	porcentaje = 100*duracionTotal/((tiempoFin-tiempoInicio)*10**6)
	lienzo.create_text(xLeyenda, yLeyenda + 32, text=str(porcentaje)+"%", fill=color(val), font=("Arial",9))
	xLeyenda = xLeyenda + deltaX

#resumen
xAbs = finLinea - 30
yAbs = yLeyenda + 20
lienzo.create_text(xAbs, yAbs, text="Elapsed Time: "+str((tiempoFin-tiempoInicio)*10**6)+" [us]", font=("Arial",10))

mainloop()
