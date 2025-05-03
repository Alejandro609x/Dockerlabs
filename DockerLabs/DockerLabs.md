Maquina:DockerLabs
Objetivo:
Descripcion: 
DockerLabs/Imàgenes/Logo.png
Primero descargamos la maquina vulnerable de dockerlabs y lo descomprimimos con el comando: unzip dockerlabs.zip y lo tenemos que desplegar con el comando: sudo bash auto_deploy.sh dockerlabs.tar
DockerLabs/Imàgenes/Capturas.png
Realizamos un ping: ping -c1 172.17.0.2 para verificar que la maquina esta activa
DockerLabs/Imàgenes/Capturas_1.png
Con la herramienta de nmapr haces un scaneo para averiguar puertos abierto usamo el comando: sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.tx y encontramos que el unico puerto abierto es el 80 http lo que sugiere que hay una pagina web
DockerLabs/Imàgenes/Capturas_2.png
Con mi scrip perosnalizable extraigo los puetos abiertos:  extractPorts allPorts.txt para usarlos en el comando: nmap -sC -sV -p 80 172.17.0.2 -oN target.txt nos sirve para que nos de mas dettale de los servicios que estan corriendo en el puerto 
DockerLabs/Imàgenes/Capturas_3.png
AL entrar a la apgina web lo primero que vemos es esto: 
DockerLabs/Imàgenes/Capturas_4.png
Nota: Al no encotrar nada significativo procedo a realizar fuzzing
Con la heraamienta de wfuzz:wfuzz -c -t 200 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt --hc 404 http://172.17.0.2/FUZZ encontre el directorio de:uploads
DockerLabs/Imàgenes/Capturas_6.png
Al poner la url completa: http://172.17.0.2/uploads/ encontre esta pagina
DockerLabs/Imàgenes/Capturas_5.png

