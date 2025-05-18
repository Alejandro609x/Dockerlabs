# **Máquina: Backend**

### **Dificultad:** Fácil

### 📝 **Descripción:**


### 🎯 **Objetivo:**


![Logo](Imágenes/2025-05-17_19-35.png)

---

## 🖥️ **Despliegue de la máquina**

Descargamos el archivo `backend.zip`, lo descomprimimos y desplegamos la máquina usando el script `auto_deploy.sh` proporcionado. Esto inicia la máquina vulnerable dentro de un contenedor Docker:

```bash
unzip backend.zip
sudo bash auto_deploy.sh backend.tar
```

![Despliegue](Imágenes/Capturas.png)

---

## 📡 **Comprobación de conectividad**

Verificamos la conexión con un simple `ping` a la IP asignada (172.17.0.3):

```bash
ping -c1 172.17.0.3
```

![Ping](Imágenes/Capturas_1.png)

---

## 🔍 **Escaneo de puertos**

Ejecutamos un escaneo de puertos completo con `nmap`:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.3 -oG allPorts.txt
```

Puertos descubiertos:

* **22/tcp** – SSH
* **80/tcp** – HTTP

![Puertos](Imágenes/Capturas_2.png)

Posteriormente, realizamos un escaneo más detallado sobre los puertos encontrados:

```bash
nmap -sCV -p22,8009,8080 172.17.0.3 -oN target.txt
```

![Servicios](Imágenes/Capturas_3.png)

---

Entre http://172.17.0.3/ en donde se encuntra alojado una pagina web donde se ecnotro que existe un login.html 
![Pagina](Imágenes/Capturas_4.png)

---

![login](Imágenes/Capturas_5.png)

Comprobación de inyección SQL en el formulario de login

Durante la fase de pruebas, se introdujo el carácter ' al final del campo de nombre de usuario en el formulario de inicio de sesión, lo cual provocó un error,Este mensaje de error revela que el sistema construye la consulta SQL de manera insegura, concatenando directamente el valor proporcionado por el usuario. La aparición del error de sintaxis confirma que no se están utilizando sentencias preparadas ni un adecuado filtrado de entrada, lo cual indica una vulnerabilidad a inyección SQL.
![inyeccion](Imágenes/Capturas_6.png)

---

![error](Imágenes/Capturas_7.png)


