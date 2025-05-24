# 🧠 **Informe de Pentesting – Máquina: BaluFood** 

### 💡 **Dificultad:** Fácil

### 🧩 **Plataforma:** DockerLabs


![Despliegue](Imágenes/2025-05-24_03-34.png)

---

## 📝 **Descripción de la máquina**


---

## 🎯 **Objetivo**


---

## ⚙️ **Despliegue de la máquina**

Se descarga el archivo comprimido de la máquina vulnerable y se lanza el contenedor Docker mediante el script incluido:

```bash
unzip balufood.zip
sudo bash auto_deploy.sh backend.tar
```

![Despliegue](Imágenes/Capturas.png)

---

## 📡 **Comprobación de conectividad**

Verificamos que la máquina se encuentra activa respondiendo a peticiones ICMP (ping):

```bash
ping -c1 172.17.0.2
```

![Ping](Imágenes/Capturas_1.png)

---

## 🔍 **Escaneo de Puertos**

Realizamos un escaneo completo para detectar todos los puertos abiertos:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

**Puertos detectados:**

* `22/tcp`: SSH
* `5000/tcp`: HTTP

![Puertos](Imágenes/Capturas_2.png)

Luego, analizamos los servicios y versiones asociados a esos puertos:

```bash
nmap -sCV -p22,80 172.17.0.2 -oN target.txt
```

![Servicios](Imágenes/Capturas_3.png)

---

Al ver que esta el puerto 5000 esta abierto nos vamos a http://172.17.0.2:5000/ para visualizar lo que aloja y nos damos cuenta que es la pagina de un restaurante y en la parte de abajo hay una seccion de comentarios.

![Pagina](Imágenes/Capturas_4.png)

Al navegar entre pestañas y ver la funciones que tiene como el de ver menu,realizar pedidos, logro encontrar un formulario de registro http://172.17.0.2:5000/login

![Registro](Imágenes/Capturas_5.png)

Al probar credenciales comunes logro accedes con usuario: admin Contraseña admin, nos reditige a http://172.17.0.2:5000/admin y se logra ver lo pedidos que realice previamente.

![Admin](Imágenes/Capturas_6.png)
Nota: Al poner el directorio: /admin tambien no da acceso a la pagina del adminitrador

Al revisar el codigo fuento de esta pestaña puedo notar que hay uno comentario con credenciales, <!-- Backup de acceso: sysadmin:backup123 -->

![Credenciales](Imágenes/Capturas_7.png)


