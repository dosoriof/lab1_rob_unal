%%
rosinit; %Conexión con nodo maestro
%% 
poseSub = rossubscriber('/turtle1/pose','turtlesim/Pose');%Creación del 
%suscriptor, la primera entrada es el tópico al que se suscribe y le
%segunda es el tipo de mensaje que se obtiene 
%% Mostrar valores del último mensaje obtenido
pose = receive(poseSub,10)
% x = poseSub.LatestMessage.X
% y = poseSub.LatestMessage.Y
% theta = poseSub.LatestMessage.Theta
% linearVel = poseSub.LatestMessage.LinearVelocity
% angularVel = poseSub.LatestMessage.AngularVelocity