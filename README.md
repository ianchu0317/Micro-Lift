# Micro-Lift


![Imagen de WhatsApp 2024-09-10 a las 21 27 16_95104079](https://github.com/user-attachments/assets/fccdc1b6-202c-467d-84e9-fa196e0192ba)


## Simulación de ascensor pequeño escrito en Python
Este proyecto es una simulación física de un ascensor. Para llevar a cabo esta idea se combinaron distintos aspectos tanto de electrónica, diseño y programación.
También se tuvo en cuenta la gestión, planificación y organización de manera ordenada de un proyecto. 

Se simula un edificio de 4 pisos en total. Para ello, consta de un panel de control que contiene 4 botones representando el botón de los 4 pisos para el llamado del ascensor, y además por cada piso hay un LED rojo y uno amarillo. El rojo indica la detención del ascensor mientras que el amarillo indica el movimiento del mismo. Se utiliza Raspberry PI 4b como microcontrolador de los circuitos eléctricos. 

La estructura final es completada y construida por medio de bloques, a diferencia de la planificación anterior, la cual era con madera o con cartón. El diseño de la planificación se puede encontrar en: https://github.com/ianchu0317/Micro-Lift/blob/main/design/3d_model_elevator_reference.stl


## Algoritmo del ascensor
1. Mientras haya alguien dentro o delante del elevador que quiera ir en la dirección actual, siga en esa dirección.
2. Una vez que el ascensor ha agotado las solicitudes en su dirección actual, cambia de dirección si hay una solicitud en contrario. Sino, se detiene y espera una llamada.

Descripción sacada de la siguiente página: https://revdelascensor.com/2018/10/26/la-ciencia-oculta-de-los-ascensores/

## Uso
### Materiales y componentes
Los materiales empleados fueron: 
- Raspberry PI 4b
- Protoboard
- 4 pulsadores de 4 pines
- 4 resistores 10k ohm (para pull down) y 8 resistores 220 ohm (para leds)
- 4 LEDs rojos y 4 LEDs amarillos
- Driver L298n (para motor dc)
- Motor dc
- Batería 
- Cables jumper macho-hembra (10 cm) y macho-macho (20 cm)

### Diagrama de circuitos
![circuit_diagram_with_motor_bb](https://github.com/user-attachments/assets/c3751c11-1616-455f-b39b-c16443040974)
NOTA: se conectan los pines del RPi según la numeración de Broadcom (BCM).

### Dimensión física de la estructura (final, no ideal)
![Imagen de WhatsApp 2024-09-10 a las 21 49 46_4862381e](https://github.com/user-attachments/assets/376c6f65-90ea-4c64-b1db-dd05fb5ce044)

Las medidas según eje: 
- X: 6 cm
- Y: 12 cm
- Z: 6 cm

Al modificar la medida de altura, será necesario cambiar la variable de `tiempo_en_movimiento` acorde al tiempo necesario para mover el ángulo deseado. Se consigue calculando `ángulo a mover / velocidad angular`. Y el ángulo a mover se consigue de la siguiente manera: `ángulo a mover (rad) = longitud de soga / radio de polea`; mientras que la velocidad angular depende del voltaje utilizado para alimentar el motor (según especificación del fabricante), que en este caso corresponde a 2.88 V - 125 RPM. 

### Uso del Software
#### Iniciar programa
Una vez iniciado sesión en la Raspberry Pi y conectados los pines GPIO de manera correcta, simplemente correr el siguiente código: 

`python controller.py`
#### Finalizar programa
Para finalizar programa se debe aplicar `Ctrl + C` para detener el bucle principal y posteriormente la tecla `Enter` para salir del programa.

## Origen de la idea del proyecto (para mí)
La idea surgió al principio del año cuando decidí estudiar programación y cuestionar acerca de los algoritmos fundamentales que frecuentamos diariamente (semáforos, ascensores, sistema de estacionamiento, etc). Más tarde, también descubrí que me gustaba poder hacer proyectos y temas como electrónica (básica) para hacer robótica y domótica. 

## Complicaciones (para mí)
- Utilización de un motor DC específico y no el deseado -> Se tuvo que utilizar otro motor y no el deseado debido a que el programa detectaba pulsaciones falsas debido a corrientes de sobra (creo).
- Finalización de proyecto de manera apurada -> la decisión de finalizar el proyecto se tomó debido a que se hacía cada vez más denso y pesado seguir las planificaciones que yo mismo hacía (xd), además de tener que mantener organizado todo lo académico. También se dificultó mucho conseguir los materiales deseados y ya no tenía ganas de continuar. Se me hizo muy difícil seguir programando ya que cada vez que abría el script para modificar estaba todo desordenado y no sabía si era acorde o no a las convenciones y también hasta mí me mareaba.
