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


Se proce a usar Jon The Riper
1. **Extraer hash**:

   ```bash
   zip2john secretitopicaron.zip > hash.txt
   ```

   *Convierte el archivo ZIP cifrado en un hash que John puede usar.*

2. **Crackear el hash**:

   ```bash
   john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
   ```

   *John usa un diccionario para encontrar la contraseña del archivo ZIP.*

3. **Mostrar la contraseña**:

   ```bash
   john --show hash.txt
   ```

   *Muestra la contraseña crackeada del archivo.*
En este caso la contraseña es: password1



Al descpmpremir el .zip nos da un archivo password con el contenido: mario:laKontraseñAmasmalotaHdelbarrioH que podemos suponer son las credenciales para el servicio de SSH
Nota: antes realice fuerza bruta con hydra con el servicio de SSH sin exito


Se entro al SSH con las credenciales encontradas y ejecute el comando sudo -l docne encotre: (ALL) NOPASSWD: /usr/bin/node /home/mario/script.js y me ubique en el directorio donde se encotraba el script.js con cd /home/mario y lo edite ya que este 
script tiene permisos y lo ejecute con: sudo node /home/mario/script.js y abri una terminal con root con el comando: bash -p
