# 🖥️ **Máquina: Obsession**  
- **🔹 Dificultad:** Muy Fácil  
- **📌 Descripción:**  
  Laboratorio para principiantes en ciberseguridad, Se trabajo son servicios SSH y FTP.

- **🎯 Objetivo:**  
  - Identificar y explotar fallos de seguridad en la aplicación backend mediante técnicas de **inyección SQL**.  
  - Comprender el impacto de estas vulnerabilidades.  

![Máquina Backend](/Obsession/Imagenes/Plantilla.png)

---

## 🚀 **Despliegue de la Máquina Obsession en DockerLabs**  

Para iniciar la máquina, sigue estos pasos:

### 1️⃣ **Descargar y descomprimir el archivo**  
Comienza descargando el archivo `.zip` y extráelo. En mi caso, utilizo `7z`:

```bash
7z e backend.zip
```

### 2️⃣ **Ejecutar el despliegue automático**  
Una vez descomprimido el archivo, ejecuta el siguiente comando para desplegar la máquina:

```bash
bash auto_deploy.sh obsession.tar
```

---

📌 **Nota:** Asegúrate de tener `7z` instalado y de ejecutar el script en un entorno adecuado con Docker configurado.  

![Máquina Iniciada](/Obsession/Imagenes/Despliegue.jpeg)

Una vez iniciada, comprueba la conexión realizando un ping con el siguiente comando:

```bash
ping -c4 172.17.0.2
```
![PING](/Obsession/Imagenes/Ping.jpeg)

Cuando la conexión esté confirmada, comenzamos la fase de reconocimiento con:

```bash
nmap -p- --open -sS --min-rate 500 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```
![Reconocimiento](/Obsession/Imagenes/Puertos.jpeg)

📌 **Nota:** En mis repositorios encontrarás scripts personalizados con los comandos utilizados en esta fase.

Para extraer la información relevante de los resultados de escaneo, utilizo el siguiente comando:

```bash
extracPorts allPorts.txt
```

Con los puertos identificados, realizamos un análisis más detallado con el siguiente comando para obtener información sobre los servicios que están corriendo en dichos puertos:

```bash
nmap -p22,80 -sCV 172.17.0.2 -oN target
```
![Reconocimiento](/Obsession/Imagenes/Servicios.jpeg)
📌 **Nota:** Esta información nos permite identificar posibles vulnerabilidades basadas en las versiones de los servicios, como en este caso, donde el puerto 22 está relacionado con SSH y el puerto 80 con una página web.

Con este analisis puedo ver que el servicio ftp no necesita contraseña ya que esta habilitado el usuario anonymus, asi que entramos con el siguiente comando y cuando pida la contraseña solo le damos enter:
```bash
ftp 172.17.0.2
```
![Reconocimiento](/Obsession/Imagenes/FTP.jpeg)
 Una vez dentro del servico encontre dos documetos que descargue en mi equipo para analizarlos con los comandos:

```bash
get pendientes.txt /home/alejandro/Descargas pendientes.txt
```
```bash
get chat-gonza.txt /home/alejandro/Descargas pendientes.txt
```
 
![Servicios](/Obsession/Imagenes/FTP descargas.jpeg)

Durante la fase de reconocimiento, detecté que el puerto 80 está abierto, lo que indica que hay un servidor web en ejecución.
Para acceder a la página web desde el navegador, es necesario añadir la dirección IP de la máquina (172.17.0.2) en el archivo hosts.
Para hacerlo, edita el archivo con el siguiente comando:

```bash
sudo nano /etc/hosts
```
Luego, añade una línea como la siguiente:

```bash
172.17.0.2    nombre-del-sitio.local
```
Guarda los cambios y podrás acceder a la página ingresando http://nombre-del-sitio.local en tu navegador.

![Pagina](/Backend/Images/etchost.jpeg)

Para recopilar información sobre la página web puedes usar el siguiente comando, lo que nos permitirá conocer los servicios y versiones utilizados, y buscar posibles vulnerabilidades:

```bash
whatweb 172.17.0.2
```

Para encontrar posibles directorios ocultos en el servidor web, utilizamos la herramienta **wfuzz** junto con una lista de palabras conocida.  
El siguiente comando realiza un ataque de fuerza bruta sobre las rutas del servidor:

```bash
wfuzz -c -t 200 -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt --hc 404 http://172.17.0.2/FUZZ
```

📌 **Explicación del comando:**
- `-c`: Muestra la salida en colores, facilitando la lectura de resultados.
- `-t 200`: Lanza hasta 200 hilos concurrentes para acelerar el proceso.
- `-w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt`: Especifica la lista de palabras que se utilizará para intentar encontrar directorios.
- `--hc 404`: Oculta las respuestas con código 404 (no encontrado) para centrarnos solo en los resultados relevantes.
- `http://172.17.0.2/FUZZ`: El punto donde **wfuzz** insertará las palabras del diccionario para probar diferentes rutas.

📎 **Nota:** Si no tienes instalada la lista de directorios (**Seclists**), puedes descargarla directamente desde GitHub con:

```bash
git clone https://github.com/danielmiessler/SecLists.git /usr/share/seclists
```
Así tendrás acceso a muchísimas listas útiles para pentesting.

![Pagina](/Obsession/Imagenes/wfuzz.jpeg)




