# 🧠 **Informe de Pentesting – Máquina: InfluencerHate**

### 💡 **Dificultad:** Fácil

📦 **Plataforma:** DockerLabs

![Despliegue](Imagenes/logo.png)
---

# 🚀 **Despliegue de la Máquina**

Para iniciar la máquina vulnerable, primero descomprimimos el archivo proporcionado y posteriormente ejecutamos el script de despliegue:

```bash
unzip influencerhate.zip
sudo bash auto_deploy.sh influencerhate.tar
```

![Despliegue](Imagenes/despliegue.png)

---

# 📶 **Comprobación de Conectividad**

Una vez desplegada la máquina, verificamos que el objetivo se encuentre activo y responda correctamente a peticiones ICMP:

```bash 
ping -c1 172.17.0.2
```

Esto nos permite confirmar que la máquina está encendida y accesible dentro de la red local del laboratorio.

![Despliegue](Imagenes/ping.png)

---

# 🔍 **Escaneo de Puertos**

## 🔎 Escaneo Completo de Puertos

Se realiza un escaneo completo sobre todos los puertos TCP para identificar los servicios expuestos en la máquina víctima:

```bash 
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2
```

### 📌 Puertos Abiertos Detectados

* `22/tcp` → Servicio SSH
* `80/tcp` → Servicio HTTP 

![Despliegue](Imagenes/nmapuno.png)
---

## 🧩 Enumeración de Servicios y Versiones

Después de identificar los puertos abiertos, procedemos a detectar versiones y configuraciones de los servicios activos:

```bash 
nmap -sCV -p22,80,3306 172.17.0.2
```

Este análisis permite obtener información más detallada sobre los servicios en ejecución, versiones instaladas y posibles configuraciones vulnerables.

![Despliegue](Imagenes/nmapdos.png)

---
