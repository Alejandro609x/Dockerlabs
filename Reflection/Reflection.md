# 🧠 **Informe de Pentesting – Máquina: Reflection**

### 💡 **Dificultad:** Fácil

### 🧩 **Plataforma:** DockerLabs

### 🕵️‍♂️ **Tipo de ataque:** Inyección SQL + Escalada de privilegios con SUID


![Despliegue](Imágenes/2025-05-18_22-56.png)

---

## 📝 **Descripción de la máquina**


---

## 🎯 **Objetivo**

---

## ⚙️ **Despliegue de la máquina**

Se descarga el archivo comprimido de la máquina vulnerable y se lanza el contenedor Docker mediante el script incluido:

```bash
unzip reflection.zip
sudo bash auto_deploy.sh reflection.tar
```

![Despliegue](Imágenes/Capturas.png)

---

## 📡 **Comprobación de conectividad**

Verificamos que la máquina se encuentra activa respondiendo a peticiones ICMP (ping):

```bash
ping -c1 172.17.0.3
```

![Ping](Imágenes/Capturas_1.png)

---

## 🔍 **Escaneo de Puertos**

Realizamos un escaneo completo para detectar todos los puertos abiertos:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.3 -oG allPorts.txt
```

**Puertos detectados:**

* `22/tcp`: SSH
* `80/tcp`: HTTP

![Puertos](Imágenes/Capturas_2.png)

Luego, analizamos los servicios y versiones asociados a esos puertos:

```bash
nmap -sCV -p22,80 172.17.0.3 -oN target.txt
```

![Servicios](Imágenes/Capturas_3.png)

---

Nos vamos al servicio web que esta alojado en http://172.17.0.3/ y encontramos unos laboratorios XXS
![Web](Imágenes/Capturas_4.png)

Entramos a Laboratorio de XSS Reflejado y escribo un encabezado <h1>Prueba insertar html</h1> y vemos que lo ejecuta
![Web](Imágenes/Capturas_6.png)

---

![Web](Imágenes/Capturas_5.png)


