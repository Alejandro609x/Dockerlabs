# 🧠 Informe de Pentesting – Máquina: Balulero

### 💡 Dificultad: Fácil

### 🧩 Plataforma: DockerLabs

![Despliegue](Imagenes/logo.png)

---

# ⚙️ Despliegue de la máquina

Antes de iniciar el proceso de reconocimiento y explotación, se procede a desplegar la máquina vulnerable proporcionada por DockerLabs.

La máquina se distribuye comprimida en formato `.zip`, conteniendo una imagen Docker y un script automatizado que facilita su ejecución.

```bash
unzip balulero.zip
sudo bash auto_deploy.sh balulero.tar
```

Una vez finalizado el despliegue, la máquina queda disponible dentro de la red local de Docker.

![Despliegue](Imagenes/despliegue.png)

---

# 📡 Comprobación de conectividad

Antes de comenzar la fase de enumeración, es importante verificar que el objetivo se encuentre activo y responda correctamente dentro de la red.

```bash
ping -c4 172.17.0.2
```

### Explicación:

* **ping** → Herramienta utilizada para verificar conectividad mediante ICMP.
* **-c4** → Envía únicamente un paquete ICMP.

La recepción de respuesta confirma:

* Existencia del host objetivo
* Conectividad de red funcional
* Baja latencia, esperada al ejecutarse dentro de Docker

![Despliegue](Imagenes/ping.png)

---

