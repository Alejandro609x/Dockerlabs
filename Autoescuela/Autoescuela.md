# 🧠 **Informe de Pentesting – Máquina: Autoescuela**

### 💡 **Dificultad:** Fácil

📦 **Plataforma:** DockerLabs

![Despliegue](Imagenes/logo.png)

---

# 🚀 **Despliegue de la Máquina**

Para desplegar la máquina vulnerable, primero descomprimimos el archivo proporcionado y posteriormente ejecutamos el script encargado de levantar el entorno Docker:

```bash
unzip autoescuela.zip
sudo bash auto_deploy.sh autoescuela.tar
```

Este proceso iniciará automáticamente los contenedores necesarios para la simulación.

![Despliegue](Imagenes/despliegue.png)

---

# 📶 **Comprobación de Conectividad**

Antes de comenzar la fase de reconocimiento, verificamos conectividad con la máquina objetivo mediante solicitudes ICMP:

```bash
ping -c1 172.17.0.2
```

La respuesta confirma que el host se encuentra activo dentro del segmento de red.

![Despliegue](Imagenes/ping.png)

---

# 🔍 Escaneo de Puertos

## 🔎 Enumeración Inicial de Servicios

Se realiza un escaneo completo sobre todos los puertos TCP con el objetivo de identificar servicios expuestos:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2
```

Parámetros utilizados:

* `-p-` → Escaneo completo de puertos.
* `--open` → Mostrar únicamente puertos abiertos.
* `-sS` → SYN Scan.
* `--min-rate 5000` → Incrementa velocidad del escaneo.
* `-n` → Evita resolución DNS.
* `-Pn` → Omite descubrimiento ICMP.

![Despliegue](Imagenes/nmapuno.png)

---

## 📌 Puertos Detectados

Durante la enumeración se identifican los siguientes servicios:

* `8080/tcp` → HTTP
* `9229/tcp` → Node.js (explica en 54 palabar el servicio deeste puerto)

![Despliegue](Imagenes/nmapdos.png)

---

## 🧩 Enumeración de Servicios y Versiones

Con los puertos identificados procedemos a obtener versiones y banners:

```bash
nmap -sCV -p8080,9229 172.17.0.2
```
---

# 🧭 Reconocimiento Web

## 🖥️ Acceso Inicial

Accedemos a la aplicación web:

```bash
http://172.17.0.2
```

El sitio responde correctamente aunque presenta contenido limitado.

![Despliegue](Imagenes/pagina.png)

---
