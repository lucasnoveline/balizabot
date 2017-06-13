#!/usr/bin/env python
# Programa de controle dos motores e do servo
# Importando bibliotecas
import RPi.GPIO as IO
import time

import rospy
from std_msgs.msg import Float32MultiArray

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

# Definindo constantes

frente = 1

tras = -1

def callbackFloatReceiver(data):
    direcao1 = data.data[0]
    direcao2 = data.data[1]
    dutyMotor1 = data.data[2]
    dutyMotor2 = data.data[3]
    servoAngle = data.data[4]
    velocidade1 = 15.0 + 1.0 * direcao1 * 5.0 * dutyMotor1 / 100.0
    velocidade2 = 15.0 + 1.0 * direcao2 * 5.0 * dutyMotor2 / 100.0
    angulo = 6.5 + 3.0 * servoAngle / 100.0
    servo.ChangeDutyCycle(angulo)
    motor1.ChangeDutyCycle(velocidade1)
    motor2.ChangeDutyCycle(velocidade2)
    #print data.data[0],data.data[1]


rospy.init_node('float_receiver',anonymous=True)
rospy.Subscriber("params_values",Float32MultiArray,callbackFloatReceiver)
while not (rospy.is_shutdown()):
    rospy.spin()
