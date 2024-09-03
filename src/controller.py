import RPi.GPIO as GPIO
from time import sleep


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


# Función que manipula entrada de un boton
def al_presionar(pin_boton):
	global en_espera
	global en_movimiento

	piso = BOTONES.index(pin_boton)
	
	# añadir piso a espera si no está 
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


# Función de actualizar variables globales
def actualizar_variables_por_piso(piso):
	global piso_actual
	global pin_led_amarillo_actual
	global pin_led_rojo_actual 

	piso_actual = piso 
	pin_led_amarillo_actual = LEDS_AMARILLOS[piso_actual]
	pin_led_rojo_actual = LEDS_ROJOS[piso_actual]


# Función de mover al piso por nº de index
def mover_a(piso):
	global piso_actual
	global en_espera
	global en_movimiento

	# Mover a cada piso
	for p in range(piso_actual, piso + direccion_actual, direccion_actual):
		actualizar_variables_por_piso(p)

		#print(f"Actualmente en piso {piso_actual}")
		#print(f"Lista de espera es: {en_espera}")
		prender_led(pin_led_amarillo_actual)
		
		# Chequear pisos intermedios si está en espera
		if p in en_espera and p != piso:
			prender_led(pin_led_rojo_actual)
			sleep(tiempo_en_espera)
			apagar_led(pin_led_rojo_actual)
			en_espera.remove(piso_actual)

		# cambio de piso
		sleep(tiempo_en_movimiento)  # Movimiento a piso siguiente
		apagar_led(pin_led_amarillo_actual)

	en_espera.remove(piso)

	if len(en_espera) == 0:
		en_movimiento = False  # Detener movimiento si no hay más pisos que ir


def loop():
	try:
		while True:
			if en_movimiento:
				apagar_led(pin_led_rojo_actual)
				# Mover al piso solicitado
				for p in en_espera:
					chequear_direccion(p)
					mover_a(p)
			else:
				# Detener el movimiento
				# Prender luz roja y amarilla
				prender_led(pin_led_rojo_actual)
				prender_led(pin_led_amarillo_actual)
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

# Variables del programa
en_espera = []  # Valores numéricos de nº index
en_movimiento = False  # Inicio detenido
tiempo_en_movimiento = 2 # 2s de movimiento entre cada piso
tiempo_en_espera = 3  # 3s de espera de entrepiso
direccion_actual = 1   # 1: arriba, -1: abajo
piso_actual = 0
pin_led_amarillo_actual = LEDS_AMARILLOS[piso_actual]
pin_led_rojo_actual = LEDS_ROJOS[piso_actual]  


# Ejecución
loop()
input("...")

# Salida y cierre del programa
print("Saliendo del programa...")
GPIO.cleanup()
