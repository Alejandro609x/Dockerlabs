# Informe de Pentesting – Máquina *Walking Dead*

**Dificultad:** Fácil  
**Fuente:** Dockerlabs  
**Objetivo:** Identificar y explotar vulnerabilidades presentes en la máquina *Walking Dead*  
**Ruta de evidencias:** `/Walking_Dead/Imagenes/`

---

## 1. Despliegue de la Máquina

Se descargó la máquina vulnerable desde el repositorio de Dockerlabs. Posteriormente, se descomprimió utilizando:

```bash
unzip walking_dead.zip
```

Luego, se desplegó la máquina con el script proporcionado:

```bash
sudo bash auto_deploy.sh walking_dead.tar
```

![Despliegue de la máquina](/Walking_Dead/Imagenes/Despliegue.jpeg)

---

## 2. Verificación de Conectividad

Para comprobar que la máquina se encuentra activa en la red, se ejecutó un comando `ping` hacia su IP asignada (172.17.0.2):

```bash
ping -c4 172.17.0.2
```

La respuesta positiva confirmó la disponibilidad de la máquina.

![Ping exitoso](/Walking_Dead/Imagenes/Ping.jpeg)

---

## 3. Reconocimiento de Puertos

Se realizó un escaneo de puertos completo con `nmap` para identificar servicios expuestos:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

Este comando escanea todos los puertos TCP abiertos mediante un escaneo SYN (`-sS`) sin realizar resolución DNS (`-n`) ni ping previo (`-Pn`). La salida se guardó en formato `grepable`.

Se identificaron los siguientes puertos abiertos:

- **22/tcp** – SSH  
- **80/tcp** – HTTP

![Puertos abiertos](/Walking_Dead/Imagenes/Puertos.jpeg)

---

## 4. Detección de Servicios y Versiones

Utilizando mi script personalizado `extractPorts`, se extrajeron los puertos detectados y se utilizó `nmap` para realizar un escaneo más detallado de servicios y versiones:

```bash
sudo nmap -sCV -p22,80 172.17.0.2 -oN targetedScan.txt
```

El parámetro `-sCV` ejecuta scripts por defecto y detecta versiones. Este análisis permitió identificar:

- **SSH**: OpenSSH con autenticación estándar (sin configuraciones inusuales)
- **HTTP**: Servidor web Apache (sin información sensible visible en headers)

![Servicios detectados](/Walking_Dead/Imagenes/Servicios.jpeg)

---

## 5. Análisis del Sitio Web

Al acceder vía navegador a `http://172.17.0.2`, el sitio inicial no muestra información útil para un atacante:

![Página principal del sitio](/Walking_Dead/Imagenes/Pagina.jpeg)

Se procedió a realizar *fuzzing* de directorios con herramientas como **Gobuster** y **Wfuzz**, pero no se encontraron recursos relevantes.

---

## 6. Análisis Manual del Código Fuente

Durante la inspección manual del código fuente HTML del sitio web, se encontró una etiqueta `<p>` oculta con un enlace sospechoso:

```html
<p class="hidden-link"><a href="hidden/.shell.php">Access Panel</a></p>
```

Este hallazgo sugiere la presencia de un posible panel oculto o incluso una *web shell*.

![Código fuente con enlace oculto](/Walking_Dead/Imagenes/Directorio_oculto.jpeg)

---

## 7. Acceso a Web Shell

Se accedió a la ruta `http://172.17.0.2/hidden/.shell.php`, donde inicialmente no se mostraba ninguna interfaz interactiva.

![Acceso a .shell.php](/Walking_Dead/Imagenes/Directorio.jpeg)

Sin embargo, se sospechó que se trataba de una *web shell* funcional basada en parámetros GET. Se probó ejecutando el siguiente comando directamente en la URL:

```
http://172.17.0.2/hidden/.shell.php?cmd=whoami
```

Esto ejecutó correctamente el comando en el sistema remoto, lo cual confirma que se trata de una *web shell* basada en parámetros. El servidor respondió con el nombre del usuario en ejecución.

![Ejecución remota del comando `whoami`](/Walking_Dead/Imagenes/web_shell.jpeg)

---

## Estado Actual

- Se ha obtenido una *web shell* funcional con acceso a la ejecución remota de comandos.
- El siguiente paso será escalar privilegios o establecer un *reverse shell* para interacción más cómoda.
- Se recomienda seguir explorando el sistema de archivos y procesos del sistema remoto.

---

¿Deseas que continúe con la post-explotación, incluyendo análisis del sistema y escalada de privilegios?
