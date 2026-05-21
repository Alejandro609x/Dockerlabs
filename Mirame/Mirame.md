# 🧠 **Informe de Pentesting – Máquina: Mirame**

### 💡 **Dificultad:** Fácil

### 🧩 **Plataforma:** DockerLabs

---

![Despliegue](Imagenes/logo.png)

---

# ⚙️ **Despliegue de la máquina**

Se descarga el archivo comprimido de la máquina vulnerable y se despliega el contenedor Docker utilizando el script proporcionado por el laboratorio:

```bash
unzip backend.zip
sudo bash auto_deploy.sh mirame.tar
```

![Despliegue](Imagenes/despliegue.png)

Primero se comprueba si se tiene conexiòn con el objetivo

![Despliegue](Imagenes/ping.png)

