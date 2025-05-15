Perfecto, mantendré **exactamente la ubicación de tus imágenes** como las tienes (`Imágenes/Nombre.png`) y mejoraré **solo la redacción** para que sea más clara, profesional y atractiva, sin mover rutas ni modificar tu contenido. Aquí tienes tu reporte reescrito respetando eso:

---

# 📄 Reporte Técnico - Máquina Vulnerable: **Candy**

**Nivel:** Fácil

---

### 🧩 Descripción y despliegue de la máquina

Se descargó la máquina vulnerable `candy.zip` y se descomprimió usando:

```bash
unzip candy.zip
```

Posteriormente, se desplegó con el siguiente comando:

```bash
sudo bash auto_deploy.sh candy.tar
```

📸
![Despliegue de la máquina](Imágenes/2025-05-14_23-56.png)

---

### 🔗 Verificación de conectividad

Se realizó un `ping` para confirmar la conexión con la IP 172.17.0.3:

```bash
ping -c1 172.17.0.3
```

📸
![Ping](Imágenes/Capturas.png)

---

### 🔍 Escaneo de puertos

Se usó Nmap para identificar puertos abiertos con el siguiente comando:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.3 -oG allPorts.txt
```

Solo se identificó el puerto 80 (HTTP).

📸
![Puertos abiertos](Imágenes/Capturas_1.png)

Luego, para obtener más detalles sobre el servicio en el puerto 80:

```bash
nmap -sC -sV -p80 172.17.0.3 -oN target.txt
```

📸
![Detalle del puerto 80](Imágenes/Capturas_2.png)

---

### 🌐 Análisis del sitio web

Al acceder a `http://172.17.0.3:80`, se visualiza un sitio con formularios de login y registro.

📸
![Sitio web principal](Imágenes/Capturas_3.png)

---

### 🗂️ Fuzzing de directorios

Se realizó un escaneo de directorios ocultos con Gobuster:

```bash
gobuster dir -u http://172.17.0.3/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20 -add-slash -b 403,404 -x php,html,txt
```

Entre los directorios descubiertos se encuentran:

```
/images /media /templates /modules /plugins /includes /language /README.txt
/components /api /cache /index.php /robots.txt /tmp /LICENSE.txt
/layouts /administrator /configuration.php /htaccess.txt /cli
```

📸
![Directorios descubiertos](Imágenes/Capturas_4.png)

---

### 👤 Descubrimiento de usuario y credenciales

En `/administrator/index.php` se encuentra el nombre de usuario \*\*
