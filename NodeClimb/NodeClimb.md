Mauina: NodeClimb
Dificultad: Facil
Descripciòn:
Objetivo:


Se descarga la maquina vulnerable de la pagina de dockerlabs y se descomprime con el comando: unzip nodeclimb.zip para desplegarce con el comando: sudo bash auto_deploy.sh nodeclimb.tar


Se realiza un ping -c1 172.17.0.3 para confirmar la conexion con la maquina vulnerable


Buscamos puertos abiertos con la herramienta de nmap sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.3 -oG allPorts.txt en este caso encontramos el puerto 21 ftp y el 22 ssh


Con mi scrip extraigo los puerto importantes: extractPorts allPorts.txt para despues hacer un scaneo exahutivo en busca de mas infoemacion como versiones: nmap -sC -sV -p21,22 172.17.0.3 -oN target.txt en este scaneo puedo ver que el servicio ftp tiene habilitado el 
usuario: Anonymous esto nos da permiso de entrar al servicio sin necesidad de tener credenciales



Se procede a entrar al servicio FTP con el usuario: Anonymous y en la contraseña le damos ENTER y obtenemos acceso



Al entar busque archvios con ls -la y encontre un .zip lo descargue con: get secretitopicaron.zip a mi maquina host y al intentar descomprimirlo con: unzip secretitopicaron.zip nos pide una contraseña



