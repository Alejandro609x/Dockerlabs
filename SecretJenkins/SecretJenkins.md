Maquina: SecretJenkins
Dificultad: Facil
![Logo](Imágenes/2025-05-15_20-59.png)

Se descarga la maquina vulnerable y se descomprime con unzip secretjenkins.zip y se despliega con el comando:  sudo bash auto_deploy.sh secretjenkins.tar
![Despliegue](Imágenes/Capturas.png)

Se realiza un ping -c1 172.17.0.3 para confirmar la conexion de la maquina 
![Ping](Imágenes/Capturas_1.png)

Se realiza scaneo con sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.3 -oG allPorts.txt y se encuentran los puertos:
22 ssh
8080 http
![Puertos](Imágenes/Capturas_2.png)

Con mi script personalisado extractPorts allPorts.txt se extrae los puertos abiertos para usarlo en nmap -sCV -p22,8080 172.17.0.3 -oN target.txt y poder ver versiones
![Servicios](Imágenes/Capturas_3.png)

Al entrar http://172.17.0.3:8080/ podemos ver un registro de login del servicio de Jenkins
![Pagina](Imágenes/Capturas_4.png)

Realizamos fuzzing gobuster dir -u http://172.17.0.3:8080 -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20 -add-slash -b 403,404 -x php,html,txt se encontro varios directorios ocultos revisamos cada uno de ellos para ver si encontramos alguna vulnerabilidad.
Nota: se cae la pagina esto nos siguiere que se podria un ataque DOS o DDOS
![Fuzzing](Imágenes/Capturas_5.png)
