# Programa de controle dos motores e do servo
# Importando bibliotecas
import RPi.GPIO as IO
import time

IO.setwarnings(False)
IO.setmode(IO.BCM)

# Estabelecendo pinos de comunicacao

IO.setup(19,IO.OUT)
IO.setup(22,IO.OUT)
IO.setup(23,IO.OUT)

# Definindo modo de operacao dos pinos

servo = IO.PWM(19,50) # Pino 19, frequencia 50 Hz
servo.start(10) # Duty cicle de inicio: 10%

motor1 = IO.PWM(22,100) # Pino 22, frequencia 100 Hz
motor1.start(15) # Duty cicle de inicio: 15%

motor2 = IO.PWM(23,100) # Pino 23, frequencia 100 Hz
motor2.start(15) # Duty cicle de inicio: 15%

led = IO.PWM(16,100) # Pino 16, frequencia 100 Hz
led.start(90) # Duty cicle de inicio: 50% 

# Definindo constantes

frente = 1

tras = -1

while True:
	
	for t in range (100):
		# Testando limites de excussao dos motores e do servo
		direcao = frente
		velocidade = 15 + 1.0*direcao*5*t/100
		angulo = 6.5 + 1.0*3*t/100
		luz = 22.5*(t%5) + 1
		servo.ChangeDutyCycle(angulo)
		motor1.ChangeDutyCycle(velocidade)
		motor2.ChangeDutyCycle(velocidade)
		led.ChangeDutyCicle(luz)
		print angulo
		print t
		time.sleep(0.1)

	for t in range (100):
		# Na diracao reversa
		direcao = tras
		velocidade = 15 + 1.0*direcao*5*t/100
		angulo = 6.5 - 1.0*3*(100-t)/100
		luz = 22.5*(t%5) + 1
		servo.ChangeDutyCycle(angulo)
		motor1.ChangeDutyCycle(velocidade)
		motor2.ChangeDutyCycle(velocidade)
		led.ChangeDutyCicle(luz)
		print angulo
		print t
		time.sleep(0.1)
