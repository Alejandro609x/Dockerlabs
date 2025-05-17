# **Máquina: HiddenCat**

### **Dificultad:** Fácil

### 📝 **Descripción:**


### 🎯 **Objetivo:**



![Logo](Imágenes/2025-05-17_13-08.png)

---

## 🖥️ **Despliegue de la máquina**

Primero descargamos la máquina vulnerable `hiddencat.zip`, la descomprimimos con `unzip` y luego la desplegamos utilizando el script proporcionado:

```bash
unzip hiddencat.zip
sudo bash auto_deploy.sh hiddencat.tar
```

Esto levanta la máquina en un entorno Docker.
![Despliegue](Imágenes/Capturas.png)

---

## 📡 **Comprobación de conectividad**

Hacemos un ping a la IP asignada (`172.17.0.3`) para confirmar que la máquina está activa:

```bash
ping -c1 172.17.0.3
```

![Ping](Imágenes/Capturas_1.png)

---

## 🔍 **Escaneo de puertos**

Ejecutamos un escaneo con `nmap` para detectar todos los puertos abiertos de la máquina:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.3 -oG allPorts.txt
```

Se detectan los siguientes puertos abiertos:

* **22 (SSH)**
* **8009 (SSH)**
* **8080 (HTTP)**
  ![Puertos](Imágenes/Capturas_2.png)

Posteriormente, con un script personalizado `extractPorts`, extraemos los puertos encontrados y los usamos para un escaneo más profundo:

```bash
nmap -sCV -p22,8080 172.17.0.3 -oN target.txt
```

![Servicios](Imágenes/Capturas_3.png)

---
