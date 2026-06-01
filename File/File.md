Maquina: File

Dificultad: Facil


![Despliegue](Imagenes/logo.png)

## ⚙️ **Despliegue de la máquina**

Se descarga el archivo comprimido de la máquina y se lanza el contenedor Docker utilizando el script proporcionado:

```bash
unzip apibase.zip
sudo bash auto_deploy.sh file.tar
```
![Despliegue](Imagenes/despliegue.png)

## 📡 **Comprobación de conectividad**

Se verifica que la máquina objetivo está activa y responde a peticiones ICMP:

```bash
ping -c1 172.17.0.3
```
![Despliegue](Imagenes/ping.png)

## 🔍 **Escaneo de Puertos**

Realizamos un escaneo de todos los puertos para detectar cuáles están abiertos:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.3 
```

**Puertos descubiertos:**

* `21/tcp`: FTP
* `80/tcp`: HTTP

![Puertos](Imagenes/nmap.png)

A continuación, analizamos los servicios y versiones presentes en los puertos detectados:

```bash
nmap -sCV -p21,80 172.17.0.3 
```

![Servicios](Imagenes/nmapdos.png)

---
