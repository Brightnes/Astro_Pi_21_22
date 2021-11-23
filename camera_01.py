"""
Piccolo programma per usare la cam
con un microscopio, in classe.
Il programma attiva un preview e
premendo ctrl c la preview viene chiusa e il programma termina
"""
from picamera import PiCamera
from sense_hat import SenseHat

camera = PiCamera()
jimmy=SenseHat()


g=(0,255,0)
b=(0,0,0)

picture_ok = [b,b,b,b,b,b,b,b,
              b,b,b,b,b,b,b,b,
              b,g,b,b,g,b,g,g,
              g,b,g,b,g,g,b,b,
              g,b,g,b,g,b,g,b,
              b,g,b,b,g,b,b,g,
              b,b,b,b,b,b,b,b,
              b,b,b,b,b,b,b,b]
#alpha è il valore di trasparenza ell'immagine; 400 e 200 indicano la posizione
# della finestra di preview; 640 e 480 sono lunghezza e larghezza della finestra.
camera.start_preview(alpha=200, fullscreen=False, window = (400, 200, 640, 480))

try:
    while True:
        jimmy.set_pixels(picture_ok)
            
except KeyboardInterrupt:
    jimmy.clear()
    camera.stop_preview()

