#!/usr/bin/env python
## Se importan las librería requeridas para la ejecución
import rospy
from geometry_msgs.msg import Twist ## Librería para poder publicar mensajes de desplazamiento
from turtlesim.srv import TeleportAbsolute, TeleportRelative ## Librería para teleportar al origen.
from std_srvs.srv import Empty ## Librería servicio limpiar pantalla.
import termios, sys, os
from numpy import pi
TERMIOS = termios

## Función para publicar los parámetros de velocidad angular lineal
def pubVel(vel_x, ang_z, t):
    ## Define el publicador con topic y Message type,
    # el parámetro qeue size limita el tamaño de la cola de mensajes
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('velPub', anonymous=False) #Inicia nodo velPub
    vel = Twist()
    vel.linear.x = vel_x # define argumento de velocidad lineal
    vel.angular.z = ang_z # define argumento de velocidad angular
    #rospy.loginfo(vel)
    # Crea límite de tiempo para publicar mensaje
    endTime = rospy.Time.now() + rospy.Duration(t)
    # Publica el mensaje durante el tiempo seleccionado
    while rospy.Time.now() < endTime:
        pub.publish(vel)

# Función para limpiar el trazo existente en la pantalla
def servClear():
    rospy.wait_for_service('/clear') # Espera al servicio clear
    try:
        serv = rospy.ServiceProxy('/clear', Empty)
        clear = serv()
    except rospy.ServiceException as e:
        print(str(e))
# Funcion para teloportar de forma absoluta.
def servTeleportAbsolute(x, y, ang):
    rospy.wait_for_service('/turtle1/teleport_absolute') # Espera por el servicio
    try:
        ## Define el publicador con topic y Message type, TeleportAbsolute
        serv = rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)
        # Define las coordenadas absolutas y el ángulo para la teleportación
        teleport = serv(x, y, ang) 
    except rospy.ServiceException as e:
        print(str(e))

## Función para teleportar relativamente se usa para rotar 180 deg
def servTeleportRelative(linear, angular):
    rospy.wait_for_service('/turtle1/teleport_relative') # Espera por el servicio
    try:
        ## Define el publicador con topic y Message type, TeleportRelative
        serv = rospy.ServiceProxy('/turtle1/teleport_relative', TeleportRelative)
        # Define la distancia relativa y el ángulo para la teleportación
        # De forma especifica solo se usa para girar 180 deg.
        teleport = serv(linear, angular)
    except rospy.ServiceException as e:
        print(str(e))

## Función para escuchar el teclado y devolver la tecla que se presiona.
def getkey():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
    new[6][TERMIOS.VMIN] = 1
    new[6][TERMIOS.VTIME] = 0
    termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
    c = None
    try:
        c = os.read(fd, 1)
    finally:
        termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
    return c
##Funcion main.
if __name__ == '__main__':
    while 1: ## Bucle infinito
        key = getkey()
        if key == b'w':
            pubVel(1,0,0.1) # Desplaza linealmente al frente por un tiempo de 0.1 seg
        if key == b's':
            pubVel(-1,0,0.1) # Desplaza linealmente atrás por un tiempo de 0.1 seg
        if key == b'a':
            pubVel(0,1,0.1) # Rota hacia la izquierda por un tiempo de 0.1 seg
        if key == b'd':
            pubVel(0,-1,0.1) # Rota hacia la derecha por un tiempo de 0.1 seg
        if key == b' ': # Rota 180 deg la tortuga
            servTeleportRelative(0,pi) 
        if key == b'r': # Teleporta la tortuga hasta el centro
            servTeleportAbsolute(5.54,5.54,0) 
        if key == b'c': # Limpia el trazo existente
            servClear()
    
        
