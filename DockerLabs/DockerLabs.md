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
Utilice la herramienta de gobuster para encotrar mas posibles directorios ocultos donde se encontraros 3 que podemos ocupar para una posible revell shell por php: gobuster dir -u http://172.17.0.2/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20 -add-slash -b 403,404 -x .php,.html,.txt
DockerLabs/Imàgenes/Capturas_7.png
/index.php: Esta es la pagina web que se encontro con nmpa: http://172.17.0.2/index.php
DockerLabs/Imàgenes/Capturas_9.png
/uploads: en este directorio encontrado: http://172.17.0.2/uploads/ podemos ver los directorios y archivos de la pagina que estan subidos
DockerLabs/Imàgenes/Capturas_8.png
/upload.php: Esta pagina nos muestra el mensaje cuando se carga el docuemto correctamente:http://172.17.0.2/upload.php
DockerLabs/Imàgenes/Capturas_10.png
/machine.php: esta pagina nos deja subir archivos pero cuando el codigo malicioso de revel shell de php nos mostro un mensaje de que solo admite .zi, asi que voy a poner 2 extenciones para que acepte el codigo php
DockerLabs/Imàgenes/Capturas_11.png
DockerLabs/Imàgenes/Capturas_12.png
Nota: El coddigo de revell shell lo obtuve de: https://github.com/pentestmonkey/php-reverse-shell se tiene que descargar o copiar el .php y cambiar la ip pot tu maquina host y el puerto donde vas a escuchar para activar el shell este metodo es similar al que se realizo en la maquina Elevator puesdes encotrar la maquina en mi repositorio
DockerLabs/Imàgenes/Capturas_17.png
Yo use el comando: mv php-reverse-shel.php php-reverse-shel.php.zip para cambiar las extenciones
DockerLabs/Imàgenes/Capturas_13.png
Se carga el archivo malicioso y subue
DockerLabs/Imàgenes/Capturas_14.png
Y ya no mostro el error de carga, asi que el .php se subio correctamente y podemos verificarlo en el recargando la pagina: /uploads
DockerLabs/Imàgenes/Capturas_15.png
DockerLabs/Imàgenes/Capturas_16.png
Nota: se subio el erchivo para descarga asi que vamos a probar otros metodos para subir el archivo en mi caso me sirvio poner la extencion .phar con el comando: mv php-reverse-shel.php.zip php-reverse-shel.phar
DockerLabs/Imàgenes/Capturas_19.png
DockerLabs/Imàgenes/Capturas_20.png
Antes de ejecutar el .php tienes que poner el puerto que escojisto como modo escucha con el comando: sudo nc -lvnp 443
DockerLabs/Imàgenes/Capturas_18.png
Nota: unavex esto activo ejecutas el .php
Se logro tener acceso a una shell
DockerLabs/Imàgenes/Capturas_21.png
Al usar sudo -l para buscar una escalda de privilegios descubir que no pude obtener unsa shell como root con los privilegios que tengo asi que busacmos en la maquina
ruta donde descubir cosa:
cd /opt/: habia una nota.txt con la inforciòn: Protege la clave de root, se encuentra en su directorio /root/clave.txt, menos mal que nadie tiene permisos para acceder a ella.
con esta ruta podemo saber donde esta la contraseñaasi que procedo ha hacer la escalada con la informacion que tenemos:
En el comando que ejecute:

sudo /usr/bin/cut -d "" -f1 "/root/clave.txt"

El usuario www-data puede ejecutar el comando cut como root sin contraseña debido a los privilegios configurados con sudo -l. El comando cut se usa para dividir o extraer secciones de un archivo de texto. En este caso, el archivo /root/clave.txt parece contener una clave o información relevante que se extrae con cut.

Aquí, el delimitador -d "" no es válido, ya que se espera un carácter delimitador para dividir el texto. Sin embargo, en algunas configuraciones, el uso de un delimitador vacío podría no afectar el resultado si cut simplemente devuelve todo el contenido de la primera "columna" o línea del archivo. El parámetro -f1 especifica que solo se debe extraer la primera sección del archivo, pero como el delimitador es incorrecto, puede que se esté extrayendo todo el archivo de alguna forma.
DockerLabs/Imàgenes/Capturas_22.png

