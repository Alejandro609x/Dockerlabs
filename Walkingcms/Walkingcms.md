# 🧠 **Informe de Pentesting – Máquina: Walkingcms**

### 💡 **Dificultad:** Fácil

### 🧩 **Plataforma:** DockerLabs

![Despliegue](Imagenes/logo.png)

---

# ⚙️ **Despliegue de la máquina**

Se descarga el archivo comprimido de la máquina vulnerable y se despliega el contenedor Docker utilizando el script proporcionado por el laboratorio:

```bash
unzip walkingcms.zip
sudo bash auto_deploy.sh walkingcms.tar
```

![Despliegue](Imagenes/despliegue.png)

# 📡 **Comprobación de conectividad**

Antes de iniciar el reconocimiento, verificamos que la máquina se encuentra activa y accesible en la red mediante una petición ICMP:

```bash
ping -c1 172.17.0.2
```

La respuesta confirma conectividad con el objetivo.

---

# 🔍 **Escaneo de Puertos**

Se realiza un escaneo completo de puertos TCP para identificar servicios expuestos en la máquina víctima:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 
```

## 📌 Puertos detectados

* `80/tcp` → Servicio HTTP
---

Posteriormente, se ejecuta un análisis más detallado para identificar versiones y configuraciones de los servicios encontrados:

```bash
nmap -sCV -p21,80 172.17.0.2 
```

![Despliegue](Imagenes/pingnmap.png)

---
