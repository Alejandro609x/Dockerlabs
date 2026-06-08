# 🧠 **Informe de Pentesting – Máquina: Wargame**

### 💡 **Dificultad:** Fácil

📦 **Plataforma:** DockerLabs

![Despliegue](Imagenes/logo.png)

---

# 🚀 **Despliegue de la Máquina**

Para iniciar la máquina vulnerable, primero descomprimimos el archivo proporcionado y posteriormente ejecutamos el script de despliegue:

```bash
unzip wargame.zip
sudo bash auto_deploy.sh wargame.tar
```

![Despliegue](Imagenes/Despliegue.png)

---

# 📶 **Comprobación de Conectividad**

Una vez desplegada la máquina, verificamos que el objetivo se encuentre activo y responda correctamente a peticiones ICMP:

```bash
ping -c1 172.17.0.2
```

![Despliegue](/AnonymousPingu/Imagenes/ping.png)

---

# 🔍 **Escaneo de Puertos**

## 🔎 Escaneo Completo de Puertos

Se realiza un escaneo completo sobre todos los puertos TCP para identificar los servicios expuestos en la máquina víctima:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2
```

### 📌 Puertos Abiertos Detectados

* `21/tcp` → Servicio FTP
* `80/tcp` → Servicio HTTP

---

## 🧩 Enumeración de Servicios y Versiones

Después de identificar los puertos abiertos, procedemos a detectar versiones y configuraciones de los servicios activos:

```bash
nmap -sCV -p21,80 172.17.0.2
```

![Despliegue](/AnonymousPingu/Imagenes/pabiertos.png)

![Despliegue](/AnonymousPingu/Imagenes/serviciosp.png)

Durante esta fase observamos un detalle importante:
el servicio FTP permite autenticación anónima (`Anonymous FTP login allowed`), lo que podría representar una vía de acceso inicial al sistema.

---

# 🧭 **Reconocimiento Web**

## 🖥️ Acceso Inicial a la Aplicación Web

Accedemos al servicio web desde el navegador:

```bash
http://172.17.0.2
```

La página carga correctamente y muestra una aplicación web funcional.

![Despliegue](/AnonymousPingu/Imagenes/pagina.png)

---

# 🗂️ Enumeración de Directorios

Para identificar rutas ocultas o directorios interesantes, realizamos fuzzing utilizando `gobuster`:

```bash
gobuster dir -u http://172.17.0.2/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x .env,.php,.bak,.old,.zip,.txt -b 403,404 --exclude-length 8068
```

Como resultado, se detectan múltiples directorios dentro de la aplicación.

![Despliegue](/AnonymousPingu/Imagenes/gobusteruno.png)

Entre todos los resultados encontrados, el directorio más interesante es:

```bash
/upload/
```

Este directorio resulta especialmente relevante porque podría permitir visualizar archivos subidos al servidor.
Si logramos cargar un archivo PHP malicioso, posiblemente podamos ejecutarlo directamente desde el navegador.

---
