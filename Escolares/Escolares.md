# 🧠 **Informe de Pentesting – Máquina: Escolares**

### 💡 **Dificultad:** Fácil

### 🧩 **Plataforma:** DockerLabs

![Despliegue](Imagenes/logo.png)

---

# ⚙️ **Despliegue de la máquina**

Antes de iniciar el proceso de reconocimiento y explotación, se procede a desplegar la máquina vulnerable proporcionada por DockerLabs.

La máquina se distribuye comprimida en formato `.zip`, conteniendo una imagen Docker y un script automatizado para facilitar su ejecución.

```bash
unzip escolares.zip
sudo bash auto_deploy.sh escolares.tar
```
Una vez finalizado el proceso, la máquina queda disponible dentro de la red Docker local.

![Despliegue](Imagenes/despliegue.png)

---

# 📡 **Comprobación de conectividad**

Antes de comenzar la enumeración, es importante verificar que el objetivo se encuentra encendido y responde dentro de la red.

```bash
ping -c1 172.17.0.2
```

### Explicación:

* **ping** → Utilidad utilizada para verificar conectividad ICMP.
* **-c1** → Envía únicamente un paquete.

La recepción de respuesta confirma:

* Existencia del host
* Conectividad de red
* Baja latencia esperada al encontrarse dentro de Docker

---

# 🔍 **Fase de Reconocimiento – Escaneo de Puertos**

La enumeración inicial comienza identificando los puertos expuestos.

Se realiza un escaneo completo sobre todos los puertos TCP:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2
```

## Explicación detallada de parámetros:

* **-p-** → Escanea los 65535 puertos TCP.
* **--open** → Muestra únicamente puertos abiertos.
* **-sS** → Realiza SYN Scan (Stealth Scan).
* **--min-rate 5000** → Fuerza una velocidad mínima de envío de paquetes.
* **-vvv** → Incrementa la verbosidad.
* **-n** → Evita resolución DNS.
* **-Pn** → Omite detección previa de host activo.

---

## 📌 Resultado obtenido

Se identifica únicamente:

* **22/tcp → SSH**
* **80/tcp → HTTP**

Esto indica que la superficie de ataque inicial está centrada en aplicaciones web y el servicio SSH.

---

## Enumeración de servicios

Una vez identificados los puertos abiertos, se ejecuta un escaneo más profundo:

```bash
nmap -sCV -p80 172.17.0.2
```

### Explicación:

* **-sC** → Ejecuta scripts NSE básicos.
* **-sV** → Detecta versiones.
* **-p80** → Analiza puertos concretos.

Este análisis revela que el servidor web utiliza **Apache**.

![Despliegue](Imagenes/nmap.png)

---

# 🌐 Enumeración Web

Al acceder al servicio HTTP:

```bash
http://172.17.0.2
```

Se observa la página de una escuela de ciberseguridad.

Esto normalmente indica:

![Despliegue](Imagenes/pagina.png)

---

# 🔎 Fuzzing de Directorios

Se utiliza **Gobuster** para buscar contenido oculto.

```bash
gobuster dir -u http://172.17.0.2/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x .env,.php,.bak,.old,.zip,.txt -b 403,404 --exclude-length 10701
```

## Explicación de Gobuster

Gobuster es una herramienta de fuerza bruta para descubrir:

* Directorios ocultos
* Archivos no indexados
* Backups
* Paneles administrativos

### Parámetros utilizados:

* **dir** → Modo descubrimiento web.
* **-u** → URL objetivo.
* **-w** → Wordlist.
* **-x** → Extensiones adicionales.
* **-b 403,404** → Ignora respuestas específicas.
* **--exclude-length** → Filtra falsos positivos.

---

## Resultado:

Se descubre:

```text
/wordpress
```

Accedemos:

```bash
http://172.17.0.2/wordpress
```

![Despliegue](Imagenes/wordpress.png)

La presencia de WordPress amplía considerablemente la superficie de ataque debido a:

* Plugins
* Usuarios enumerables
* Temas vulnerables
* Configuraciones inseguras

---

# 🔐 Descubrimiento del Panel Administrativo

Se continúa enumerando:

```bash
gobuster dir -u http://172.17.0.2/wordpress -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x .env,.php,.bak,.old,.zip,.txt -b 403,404 --exclude-length 10701
```

Resultado:

```text
/wp-admin
```

Acceso:

```bash
http://172.17.0.2/wordpress/wp-admin
```

Esto confirma la existencia del portal administrativo.

---

# 👤 Enumeración de Usuarios WordPress

Se utiliza WPScan.

```bash
wpscan --url http://172.17.0.2/wordpress/ --enumerate u
```

## ¿Qué es WPScan?

WPScan es una herramienta especializada en WordPress capaz de:

* Enumerar usuarios
* Detectar plugins
* Buscar vulnerabilidades
* Realizar ataques de credenciales

---

Resultado:

Usuario encontrado:

```text
luisillo
```

![Despliegue](Imagenes/wpscanuno.png)

![Despliegue](Imagenes/wpescanusuario.png)

---
