import RPi.GPIO as GPIO
from time import sleep


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


# Función que manipula entrada de un boton 
def al_presionar(pin_boton):
	global en_espera
	global en_movimiento
	piso = BOTONES.index(pin_boton)
	if piso not in en_espera:
		en_espera.append(piso)
		en_movimiento = True
	# Debug
	print(f"Botón de pin {pin_boton} pulsado, se quiere ir al piso {piso}")
	print(en_espera)


# Prender led por N-pin
def prender_led(led_pin):
	GPIO.output(led_pin, GPIO.HIGH)


# Apagar led por N-pin
def apagar_led(led_pin):
	GPIO.output(led_pin, GPIO.LOW)


# Hallar sentido de direccion comparando piso actual y destino
def chequear_direccion(piso_dest):
	global direccion_actual
	if piso_actual < piso_dest:
		direccion_actual = 1  # Dirección arriba
	else:
		direccion_actual = -1  # Dirección abajo


# Función de mover al piso por número de index
def mover_a(piso):
	global piso_actual
	global en_espera
	global en_movimiento

	# Mover a cada piso
	for p in range(piso_actual, piso + direccion_actual, direccion_actual):
		prender_led(LEDS_AMARILLOS[p])
		sleep(tiempo_en_movimiento)
		apagar_led(LEDS_AMARILLOS[p])
		piso_actual = p
		print(f"Actualmente en piso {piso_actual}")

	en_espera.remove(piso)
	en_movimiento = False


# Chequear el estado de los botones
def chequear_estado():
	if en_movimiento:
		mover_a()
		# Apagar la luz roja del piso actual
		apagar_led(LEDS_ROJOS[piso_actual])
	else:
		# Prender luz roja
		prender_led(LEDS_ROJOS[piso_actual])


def loop():
	try:
		while True:
			if en_movimiento:
				# Mover al piso solicitado
				apagar_led(LEDS_ROJOS[piso_actual])
				for p in en_espera:
					chequear_direccion(p)
					mover_a(p)
			else:
				# Detener el movimiento
				# Prender luz roja
				prender_led(LEDS_ROJOS[piso_actual])
			sleep(0.1)
	except KeyboardInterrupt:
		print("Saliendo del bucle!")


# Configuraciones globales
# Configurar GPIO
LEDS_AMARILLOS = [8, 24, 18, 14]  # LEDs que indican cambio de piso
LEDS_ROJOS = [7, 25, 23, 15]  # LEDs que indican detención de movimiento 
BOTONES = [10, 22, 27, 17]  
FUENTES = [5, 6]  # Fuentes extras 3.3v
GPIO.setup(LEDS_AMARILLOS, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LEDS_ROJOS, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(FUENTES, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(BOTONES, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
for b in BOTONES:
	GPIO.add_event_detect(b, GPIO.RISING, callback=al_presionar, bouncetime=300)
en_espera = []  # Valores numéricos de N-piso, index
en_movimiento = False  # Inicio detenido
direccion_actual = 1   # 1: arriba, -1: abajo
piso_actual = 0  
tiempo_en_movimiento = 3 # 3s Entre cada piso


# Ejecución
loop()
input("...")

print("Saliendo del programa...")
GPIO.cleanup()
