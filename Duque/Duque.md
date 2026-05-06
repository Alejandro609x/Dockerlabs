# 🧠 **Informe de Pentesting – Máquina: Duque**

### 💡 **Dificultad:** Fácil

📦 **Plataforma:** DockerLabs

🌐 **Objetivo:** (Completalo)

![Despliegue](/Duque/Imágenes/Duque.png)

---

## 🚀 **Despliegue de la Máquina**

Se inicia la máquina vulnerable descomprimiendo el archivo y ejecutando el script de despliegue:

```bash
unzip bicho.zip
sudo bash auto_deploy.sh duque.tar
```
---

## 📶 **Comprobación de Conectividad**

Validamos que la máquina responde:

```bash
ping -c1 172.17.0.2
```
---

## 🔍 **Escaneo de Puertos**

### 🔎 Escaneo Total

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 
```

**Puertos abiertos:**

* `22/tcp`: SSH
* `80/tcp`: HTTP

### 🧩 Detección de Servicios

```bash
nmap -sCV -p22,80 172.17.0.2 
```
![Puertos](/Duque/Imágenes/conectividad.png)

---

## 🧭 **Reconocimiento Web**

### 🖥️ Acceso inicial

Al acceder a `http://172.17.0.2`, se muestra una página web.

### 🗂️ Fuzzing de Directorios

```bash
gobuster dir -u http:/172.17.0.2/ \
-w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt \
-t 20 -add-slash -b 403,404 -x .php,.html,.txt
```
Se encontraron rutas que mostraba la pagina de inicio y se procede a verificar cada una de ellas

![logs](/Duque/Imágenes/gobusteruno.png) 



