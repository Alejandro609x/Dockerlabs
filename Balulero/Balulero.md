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
