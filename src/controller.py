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
	# Debug
	print(f"Botón de pin {pin_boton} pulsado, se quiere ir al piso {piso}")
	print(en_espera)


def loop():
	try:
		while True:
			sleep(0.1)
	except KeyboardInterrupt:
		print("Saliendo del bucle!")


# Configuraciones globales
# Configurar GPIO
LEDS_AMARILLOS = [8, 24, 18, 14]  # GPIO de LEDs que indican cambio de piso
LEDS_ROJOS = [7, 25, 23, 15]  # GPIO de LEDs que indican detención de movimiento 
BOTONES = [10, 22, 27, 17]  
FUENTES = [5, 6]  # Fuente extra 3.3v
GPIO.setup(LEDS_AMARILLOS, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LEDS_ROJOS, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(FUENTES, GPIO.OUT, intial=GPIO.HIGH)
GPIO.setup(BOTONES, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
for b in BOTONES:
	GPIO.add_event_detect(b, GPIO.RISING, callback=al_presionar, bouncetime=300)
en_espera = []  # Valores numéricos de N-piso, index
en_movimiento = False  # Inicio detenido
direccion_actual = 1   # 1: arriba, 0: abajo
piso_actual = 0  

input("...")

print("Saliendo del programa...")
GPIO.cleanup()
