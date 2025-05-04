Maquina: stallarjwt
Nivel: Facil
Proposito:
Objetivo:
Imagenes/Logo.png
Primero se descarga la maquina .zip vulnerable de la pagina dockerlab y lo descompremi con el comando unzip stallarjwt.zip y lo despliego con el comando: sudo bash auto_deploy.sh stellarjwt.tar
Imagenes/Capturas.png
Se procede a confirmar si tenemos activa la maquina vulnerable con un ping -c1 172.17.0.2
Imagesnes/Capturas_1.png
Con la herramienta de nmap buscaremos los puertos abiertos: sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt y encuento el puerto 22 SSH y el 80 http una posible pagina web
Imagesnes/Capturas_2.png
Con mi scrito perseonalizable extraigo los puetor importantes extractPorts allPorts.txt y con la herramienta de namp intento buscar mas informacion como versiones de los servicios que estan corriendo en los puertos
Imagesnes/Capturas_3.png
