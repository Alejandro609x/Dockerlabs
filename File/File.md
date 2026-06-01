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

