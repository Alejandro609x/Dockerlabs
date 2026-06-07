# 🧠 **Informe de Pentesting – Máquina: Internal**

### 💡 **Dificultad:** Fácil

📦 **Plataforma:** DockerLabs

![Despliegue](Imagenes/Logo.png)

---

# 🚀 **1. Despliegue del Entorno**

El primer paso consiste en desplegar la máquina vulnerable proporcionada por la plataforma. Para ello, se descomprime el archivo entregado y se ejecuta el script de automatización.

### 📦 Descompresión del laboratorio

```bash
unzip internal.zip
```

### ⚙️ Despliegue del contenedor

```bash
sudo bash auto_deploy.sh internal.tar
```
Este script inicializa el entorno Docker con la máquina objetivo, asignándole una IP interna accesible desde el host atacante.

![Despliegue](Imagenes/despliegue.png)

---

# 📶 **2. Comprobación de Conectividad**

Antes de iniciar el reconocimiento, se valida la conectividad con la máquina víctima mediante una petición ICMP.

```bash
ping -c1 172.17.0.2
```

El objetivo responde correctamente, confirmando que el host está activo y accesible dentro de la red local del entorno Docker.

![Despliegue](Imagenes/ping.png)
---


# 🔍 **3. Reconocimiento y Escaneo de Puertos**

## 📡 Escaneo completo de puertos TCP

Se realiza un escaneo agresivo de todos los puertos TCP con el objetivo de identificar servicios expuestos:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2
```

### 📌 Resultados obtenidos

* `22/tcp` → SSH (OpenSSH)
* `80/tcp` → Servicio HTTP (Apache)

Se confirma que la superficie de ataque incluye un servicio web y un servicio de acceso remoto.

---

## 🧩 Enumeración de versiones y servicios

Se ejecuta un escaneo más detallado para identificar versiones y configuración de los servicios:

```bash
nmap -sCV -p22,80 172.17.0.2
```

Este análisis permite detectar información relevante como el tipo de servidor web, posibles endpoints y configuración del servicio SSH.

![Despliegue](Imagenes/nmap.png)

---
