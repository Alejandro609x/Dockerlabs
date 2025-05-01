# Informe de Pentesting – Máquina *Walking Dead*

**Dificultad:** Fácil  
**Fuente:** Dockerlabs  
**Objetivo:** Identificar y explotar vulnerabilidades presentes en la máquina *Walking Dead*  
**Ruta de evidencias:** `/Walking_Dead/Imagenes/`

![Logo](/Walking_Dead/Imagenes/Logo.png)

---

## 1. Despliegue de la Máquina

Se descargó la máquina desde Dockerlabs. Se descomprimió y desplegó utilizando:

```bash
unzip walking_dead.zip
sudo bash auto_deploy.sh walking_dead.tar
```

![Despliegue](/Walking_Dead/Imagenes/Despliegue.jpeg)

---

## 2. Verificación de Conectividad

Se confirmó que la máquina está activa mediante un `ping` a la IP 172.17.0.2:

```bash
ping -c4 172.17.0.2
```

![Ping](/Walking_Dead/Imagenes/Ping.jpeg)

---

## 3. Escaneo de Puertos

Se utilizó `nmap` para detectar puertos abiertos:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

Se identificaron los puertos 22 (SSH) y 80 (HTTP).

![Puertos abiertos](/Walking_Dead/Imagenes/Puertos.jpeg)

---

## 4. Detección de Servicios

Con el script `extractPorts` se extrajeron los puertos abiertos para un escaneo más profundo:

```bash
sudo nmap -sCV -p22,80 172.17.0.2 -oN targetedScan.txt
```

Se identificó:

- **Apache Web Server en el puerto 80**
- **OpenSSH en el puerto 22**

![Servicios detectados](/Walking_Dead/Imagenes/Servicios.jpeg)

---

## 5. Análisis del Sitio Web

Al visitar `http://172.17.0.2`, el sitio no ofrecía información útil directamente.

![Página principal](/Walking_Dead/Imagenes/Pagina.jpeg)

Se intentó encontrar contenido oculto mediante herramientas de enumeración de directorios como **Gobuster** y **Wfuzz**, sin resultados relevantes iniciales.

---

## 6. Análisis Manual del Código Fuente

Al inspeccionar manualmente el código HTML del sitio (clic derecho > Ver código fuente), se encontró un fragmento sospechoso:

```html
<p class="hidden-link"><a href="hidden/.shell.php">Access Panel</a></p>
```

![Fragmento HTML oculto](/Walking_Dead/Imagenes/Directorio_oculto.jpeg)

Este tipo de etiquetas ocultas no son visibles en el navegador, pero están presentes en el código fuente. La etiqueta `<a href="hidden/.shell.php">` apunta a un posible recurso interesante: un archivo PHP con nombre `.shell.php`, lo que puede sugerir una **web shell**.

---

## 7. Confirmación de Web Shell

Se accedió directamente a la ruta descubierta:  
`http://172.17.0.2/hidden/.shell.php`

Inicialmente, la página mostraba una pantalla en blanco, sin interfaz aparente:

![Acceso a .shell.php](/Walking_Dead/Imagenes/Directorio.jpeg)

Sin embargo, se probó manualmente añadir el parámetro `?cmd=whoami` a la URL, lo cual ejecutó un comando del sistema remoto:

```
http://172.17.0.2/hidden/.shell.php?cmd=whoami
```

Esto reveló el usuario bajo el cual corre el servidor web: `www-data`.

![Salida del comando whoami](/Walking_Dead/Imagenes/web_shell.jpeg)

Esto **confirma que la página es una Web Shell**, y permite ejecutar comandos en el sistema remoto directamente desde el navegador.

---

## 8. Glosario de Términos Técnicos

### 🔍 Fuzzing

**Fuzzing** (también conocido como *fuzz testing*) es una técnica utilizada para descubrir directorios, archivos o parámetros ocultos en una aplicación web. Consiste en enviar automáticamente cientos o miles de peticiones con distintos nombres comunes o patrones, con la esperanza de que el servidor responda con algún resultado inesperado.

Ejemplo de herramienta de fuzzing:
```bash
gobuster dir -u http://172.17.0.2 -w /usr/share/wordlists/dirb/common.txt
```

---

### 🔐 Web Shell

Una **web shell** es un script (en PHP, ASP, etc.) que permite al atacante ejecutar comandos en el sistema a través de un navegador. Comúnmente se accede a ella mediante un parámetro en la URL como `?cmd=ls`, que se interpreta en el backend del servidor.

---

### 💡 Parámetro GET

Los parámetros GET permiten enviar datos en la URL. En este caso, `?cmd=whoami` significa que el parámetro `cmd` tiene como valor el comando `whoami`, que será ejecutado por el script del servidor.

---

## Estado Actual y Próximos Pasos

✔ Acceso exitoso a web shell  
✔ Confirmación de ejecución remota de comandos como `www-data`  
➡ Próximo paso: intentar escalar privilegios para obtener acceso como **root**
