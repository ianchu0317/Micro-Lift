import RPi.GPIO as GPIO
from time import sleep


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


# Manipular pulsación de un botón
# Entrada: PIN del botón
def al_presionar(pin_boton):
	global en_espera
	global en_movimiento

	piso = BOTONES.index(pin_boton)
	
	# Añadir piso a espera si no lo está 
	if piso not in en_espera:
		en_espera.append(piso)
		en_movimiento = True
	
	# Debug
	print(f"Botón de pin {pin_boton} pulsado, se quiere ir al piso {piso}")
	print(en_espera)


# Prender led por número de pin (BCM)
def prender_led(led_pin):
	GPIO.output(led_pin, GPIO.HIGH)


# Apagar led por número de pin (BCM)
def apagar_led(led_pin):
	GPIO.output(led_pin, GPIO.LOW)


# Motor enrollar soga
def enrollar():

	if direccion_actual:
		in_1_state = GPIO.HIGH
		in_2_state = GPIO.LOW
	else:
		in_1_state = GPIO.LOW
		in_2_state = GPIO.HIGH

	pwm.start(40)
	GPIO.output(in_1, in_1_state)
	GPIO.output(in_2, in_2_state)
	sleep(tiempo_en_espera)
	pwm.stop()


# Hallar sentido de dirección actual
# Entrada: Piso objetivo que se quiere ir (index 0-3)
def chequear_direccion(piso_dest):
	global direccion_actual
	if piso_actual < piso_dest:
		direccion_actual = 1  # Dirección arriba
	else:
		direccion_actual = -1  # Dirección abajo


# Acrtualizar variables globales para cada piso actual
def actualizar_variables_por_piso(piso):
	global piso_actual
	global pin_led_amarillo_actual
	global pin_led_rojo_actual 

	piso_actual = piso 
	pin_led_amarillo_actual = LEDS_AMARILLOS[piso_actual]
	pin_led_rojo_actual = LEDS_ROJOS[piso_actual]


# Mover al piso objetivo
# Entrada: Piso objetivo que se quiere ir (index 0-3)
def mover_a(piso):
	global piso_actual
	global en_espera
	global en_movimiento

	# Mover a cada piso (pisos intermedios)
	for p in range(piso_actual, piso + direccion_actual, direccion_actual):
		actualizar_variables_por_piso(p)

		#print(f"Actualmente en piso {piso_actual}")
		#print(f"Lista de espera es: {en_espera}")
		prender_led(pin_led_amarillo_actual)
		
		# Chequear si piso intermedio está en espera
		if p in en_espera and p != piso:
			prender_led(pin_led_rojo_actual)
			sleep(tiempo_en_espera)
			apagar_led(pin_led_rojo_actual)
			en_espera.remove(piso_actual)

		# Cambio de piso
		enrollar()
		# sleep(tiempo_en_movimiento)  # Movimiento a piso siguiente
		apagar_led(pin_led_amarillo_actual)

	en_espera.remove(piso)

	if len(en_espera) == 0:
		en_movimiento = False  # Detener movimiento si no hay más pisos


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
# Configurar GPIO (BCM)
LEDS_AMARILLOS = [8, 24, 18, 14]  	# LEDs que indican cambio de piso
LEDS_ROJOS = [7, 25, 23, 15]  		# LEDs que indican detención de movimiento 
BOTONES = [10, 22, 27, 17]  
GPIO.setup(LEDS_AMARILLOS, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LEDS_ROJOS, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(BOTONES, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
for b in BOTONES:
	GPIO.add_event_detect(b, GPIO.RISING, callback=al_presionar, bouncetime=300)

# Configuración del motor
en_a = 12
in_1 = 16
in_2 = 20
GPIO.setup([en_a, in_1, in_2], GPIO.OUT, initial=GPIO.LOW)  # Configuración de salida
pwm = GPIO.PWM(en_a, 1000)  # 1000 Hz


# Variables del programa
en_espera = []  			# Valores numéricos de nº index
en_movimiento = False  		# Inicio detenido
tiempo_en_movimiento = 2  	# 2s de movimiento entre cada piso
tiempo_en_espera = 3  		# 3s de espera de entrepiso
direccion_actual = 1   		# 1: arriba, -1: abajo
piso_actual = 0  			# 0: p1, 1: p2, 2: p3, 3: p4 
pin_led_amarillo_actual = LEDS_AMARILLOS[piso_actual]
pin_led_rojo_actual = LEDS_ROJOS[piso_actual]  


# Ejecución
loop()
input("...")

# Salida y cierre del programa
print("Saliendo del programa...")
GPIO.cleanup()
