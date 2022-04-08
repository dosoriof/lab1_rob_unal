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
rosrun hello turtle myTeleopKey.py.
```

## Conclusiones


