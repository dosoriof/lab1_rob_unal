%%
rosinit; %Conexión con nodo maestro
%%
poseServ = rossvcclient("/turtle1/teleport_absolute","turtlesim/" + ...
    "TeleportAbsolute");% Creación del cliente del servicio, la primera
%entrada es el servicio y la segunda el tipo de mensaje que recibe el
%servicio
%%
%Creación del mensaje para mandar al servicio
pose = rosmessage(poseServ); 
pose.X = 7;
pose.Y = 3;
pose.Theta = 3.14;
%Se verifica si el servicio está disponible
if isServerAvailable(poseServ)
    call(poseServ,pose,"Timeout",3) %Si el servicio está disponible se
    %e  nvía el mensaje "pose" al servicio "poserServ"
else
    error("Service server not available on network")
end