# lab1_rob_unal

Entrega Laboratorio 1 Robótica 

Integrantes:
* Rafael Ricardo Galindo León
* Diego Fabian Osorio Fonseca


## Matlab

Para comenzar se siguieron los primeros pasos de la guía:
1. Iniciar el nodo maestro escribiendo en la terminal 
```
roscore
```
2. Iniciar el nodo de la simulación de la tortuga escribiendo en la terminal
```
rosrun turtlesim turtlesim_node
```
3. Crear el script en matlab:
[![Código ejemplo Matlab](https://i.postimg.cc/LXFn2LC2/Captura-de-pantalla-de-2022-04-07-16-26-20.png)](https://postimg.cc/8Fw1bJg0)

Lo anterior hace que la simulación de la toruga mueva automáticamente su posición como se ve a continuación:
[![Mov tortuga ejemplo](https://i.postimg.cc/7LDF4L3j/Captura-de-pantalla-de-2022-04-07-16-31-56.png)](https://postimg.cc/w1ffcgbk)

Ahora vamos a hacer los códigos propuestos:

### Suscripción al tópico pose

Para hacer esto buscamos información de la función ***rossubscriber*** que es la que nos permite hacer esto, para esto buscamos la documentación del paquete de ROS para matlab

[![Documentación ROS Matlab](https://i.postimg.cc/Sx0sWW48/Captura-de-pantalla-de-2022-04-07-16-43-40.png)](https://postimg.cc/ppZRv5pX)

En el código de matlab hay que iniciar primero la conexión con el nodo maestro, para eso usamos:
```
rosinit
```
A continuación, creamos el suscriptor. Usamos la función que nombramos anteriormente ***rossubscriber***, donde su primera entrada corresponde al nodo al que queremos suscribirnos (/turtle1/pose en este caso) y el segundo es el tipo de mensaje que recibimos (/turtlesim/Pose). Para conocer el tipo de mensaje que vamos a usar podemos usar el código ***rostopic info /turtle1/pose***
```
poseSub = rossubscriber('/turtle1/pose','turtlesim/Pose');
```
Ahora, para visualizar la información recibida tenemos dos opciones:
* En el atributo LatestMessage del suscriptor que acabamos de crear podemos encontrar el mensaje que se recibió:
```
x = poseSub.LatestMessage.X
y = poseSub.LatestMessage.Y
theta = poseSub.LatestMessage.Theta
linearVel = poseSub.LatestMessage.LinearVelocity
angularVel = poseSub.LatestMessage.AngularVelocity
```
* Podemos usar la función ***receive*** para ver el mensaje del sucriptor, con la segunda entrada siendo un time-out en segundos:
```
pose = receive(poseSub,10)
```
Con esto hemos creado un nodo suscriptor al tópico */turtle1/pose* que nos permite obtener la posición de la tortuga en la ventana. En la siguiente gráfica podemos ver el nodo poseSub de matlab conectándose al tópico.

[![Gráfica nodos y tópicos](https://i.postimg.cc/VNTm8CR4/Captura-de-pantalla-de-2022-04-07-17-39-23.png)](https://postimg.cc/KKnd74Cg)

#### Servicio Teleport
De igual manera, hacemos uso de la documentación de la extensión de ROS en matlab para conocer como acceder al servicio. 
Si no hemos iniciado la conexión con el nodo maestro de Matlab, tenemos que correr en Matlab el siguiente comando:
```
rosinit
```
Como el servicio para modificar la posición */turtle1/teleport_absolute* ya se encuentra creado, lo que tenemos que hacer es crear un cliente para ese servicio que envíe un mensaje con la posición a la que queremos ir. Para esto, primero tenemos que crear el cliente con la función ***rossvcclient***, que recibe el nombre del servicio y el tipo de mensaje *turtlesim/TeleporAbsolute*. Se puede buscar el tipo de mensaje usando el comando ***rosservice info /turtle1/teleport_absolute***
```
poseServ = rossvcclient("/turtle1/teleport_absolute","turtlesim/TeleportAbsolute");
```
Ahora creamos el mesanje que queremos mandar, para esto usamos la función ***rosmessage*** e ingresamos como parámetro el servicio. Llemanos el mensaje con los datos ue queremos mandar:
```
pose = rosmessage(poseServ); 
pose.X = 7;
pose.Y = 3;
pose.Theta = 3.14;
```
Finalmente solo queda hacer el llamado del servicio con la función ***call*** que recibe el servicio, el mensaje y un time-out
```
if isServerAvailable(poseServ)
    call(poseServ,pose,"Timeout",3)
else
    error("Service server not available on network")
end
```
[![Captura-de-pantalla-de-2022-04-07-18-07-38.png](https://i.postimg.cc/44HMM0qD/Captura-de-pantalla-de-2022-04-07-18-07-38.png)](https://postimg.cc/6TwY4M9c)

### Finalizar el nodo maestro en Matlab
Según la documentación del toolbox de ROS, para hacer la finalización del nodo hay que correr el siguiente código:
```
rosshutdown
```

[![Captura-de-pantalla-de-2022-04-07-18-16-12.png](https://i.postimg.cc/c4szHJrS/Captura-de-pantalla-de-2022-04-07-18-16-12.png)](https://postimg.cc/8s04XNRK)

## ROS - Python
En la segunda parte de este laboratorio vamos a crear un script en python que permita realizar las siguientes funciones:
* Se debe mover hacia adelante y hacia atrás con las teclas W y S
* Debe girar en sentido horario y antihorario con las teclas D y A.
* Debe retornar a su posición y orientación centrales con la tecla R
* Debe dar un giro de 180° con la tecla ESPACIO
* Adicionalmente se agrega una función de limpiar el espacio de la tortuga con la letra C

Para hacer el desarrollo de las anteriores funcionalidades se creó el script ***myTeleopKey.py*** en python, el cual se debe correr como se indicará más adelante.
El script ***myTeleopKey.py*** esta compuesto por las siguiente partes. Cada una de las partes está explicada con el código comentado
#### Importaciones
``` python
## Se importan las librería requeridas para la ejecución
import rospy
from geometry_msgs.msg import Twist ## Librería para poder publicar mensajes de desplazamiento
from turtlesim.srv import TeleportAbsolute, TeleportRelative ## Librería para teleportar al origen.
from std_srvs.srv import Empty ## Librería servicio limpiar pantalla.
import termios, sys, os
from numpy import pi
TERMIOS = termios
```

#### Funcion para publicar la velocidad
``` python
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
```

#### Funcion para Limpiar el trazo existente de la tortuga
``` python
# Función para limpiar el trazo existente en la pantalla
def servClear():
    rospy.wait_for_service('/clear') # Espera al servicio clear
    try:
        serv = rospy.ServiceProxy('/clear', Empty) # Llamar el servicio
        clear = serv()
    except rospy.ServiceException as e:
        print(str(e))
```

#### Funcion para teleportar al origen
``` python
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
```

#### Funcion para rotar 180 deg
``` python
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
```

#### Funcion para obtener las entradas de teclado
``` python
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
```

#### Funcion MAIN
``` python
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
```
### Correr el script
Para correr el script primero necesitamos iniciar el nodo maestro. Corremos en una terminal:
```
roscore
```
Ahora tenemos que cargar el paquete, para eso ejecutamos lo siquiente en otra terminal:
```
cd ~/catkin_ws
catkin build hello_turtle
```
Luego, sourceamos:
```
source devel/setup.bash
```
Con esto hecho, vamos a correr el nodo de la simulación de la tortuga:
```
rosrun turtlesim turtlesim_node 
```
Finalmente lanzamos nuestro script ***myTeleopKey*** y ya podemos empezar a mover la tortuga como se indicó anteriormente:
```
rosrun hello_turtle myTeleopKey.py
```

## Conclusiones
* Matlab y Python son herramientas muy poderosas para el trabajo con ROS, estas permiten desde diferentes ambientes crear, usar y modificar elementos tales como nodos, tópicos y servicios. En estas herramientas se pueden ejecutar varias ordenes en un solo script, que hacen la interacción entre el usuario y el sistema mucho más fácil.
* Al aumentar la complejidad de los scripts y códigos en Matlab se pueden obtener sistemas muy automáticos, que permitan interactuar con los componentes de ROS de forma más natural y eficiente, adicionalmente nos permiten usar herramientas que estén desarrolladas en otros softwares o lenguajes; aumentando así las funcionalidades básicas de ROS.


