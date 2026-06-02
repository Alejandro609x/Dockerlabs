# 🧠 **Informe de Pentesting – Máquina: Showtime**

### 💡 **Dificultad:** Fácil

### 🧩 **Plataforma:** DockerLabs

![Despliegue](Imagenes/logo.png)

---

# ⚙️ **Despliegue de la máquina**

Antes de iniciar el proceso de reconocimiento y explotación, se procede a desplegar la máquina vulnerable proporcionada por DockerLabs.

La máquina se distribuye comprimida en formato `.zip`, conteniendo una imagen Docker y un script automatizado para facilitar su ejecución.

```bash
unzip showtime.zip
sudo bash auto_deploy.sh showtime.tar
```
Una vez finalizado el proceso, la máquina queda disponible dentro de la red Docker local.

![Despliegue](Imagenes/despliegue.png)

---
