# 🧠 **Informe de Pentesting – Máquina: Reflection**

### 💡 **Dificultad:** Fácil

### 🧩 **Plataforma:** DockerLabs

### 🕵️‍♂️ **Tipo de ataque:** Inyección XSS (Reflejado, Almacenado, GET y Dropdowns) + Escalada de privilegios con binario SUID

![Despliegue](Imágenes/2025-05-18_22-56.png)

---

## 📝 **Descripción de la máquina**

Reflection es una máquina vulnerable alojada en DockerLabs que simula escenarios reales de seguridad web, particularmente enfocados en vulnerabilidades de tipo Cross-Site Scripting (XSS) en diferentes formas: reflejado, almacenado, en parámetros GET y en menús desplegables. También incorpora un escenario de escalada de privilegios local mediante un binario con permisos SUID, permitiendo obtener acceso como usuario root.

---

## 🎯 **Objetivo**

El objetivo principal es identificar y explotar diferentes tipos de vulnerabilidades XSS presentes en la aplicación web y, posteriormente, escalar privilegios desde un usuario normal hasta obtener acceso root en el sistema.

---

## 🎯 **Propósito del laboratorio**

Este laboratorio está diseñado para afianzar conceptos de seguridad ofensiva mediante la explotación de vulnerabilidades web (XSS) y técnicas de escalada de privilegios en sistemas Linux. Permite practicar el análisis de aplicaciones inseguras y obtener acceso completo al sistema comprometido.

---

## ⚙️ **Despliegue de la máquina**

Se descarga el archivo comprimido y se lanza el contenedor con el siguiente script:

```bash
unzip reflection.zip
sudo bash auto_deploy.sh reflection.tar
```

![Despliegue](Imágenes/Capturas.png)

---

## 📡 **Comprobación de conectividad**

Verificamos que la máquina está activa y responde correctamente a solicitudes ICMP:

```bash
ping -c1 172.17.0.3
```

![Ping](Imágenes/Capturas_1.png)

---

## 🔍 **Escaneo de Puertos**

Realizamos un escaneo completo de puertos con Nmap:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.3 -oG allPorts.txt
```

**Puertos abiertos detectados:**

* `22/tcp`: SSH
* `80/tcp`: HTTP

![Puertos](Imágenes/Capturas_2.png)

Posteriormente, analizamos los servicios y versiones con:

```bash
nmap -sCV -p22,80 172.17.0.3 -oN target.txt
```

![Servicios](Imágenes/Capturas_3.png)

---

## 🌐 **Análisis del Servicio Web**

Accedemos al sitio web en `http://172.17.0.3/` y observamos que contiene varios laboratorios vulnerables a ataques XSS.

![Web](Imágenes/Capturas_4.png)

---

## 🧪 **XSS Reflejado**

Ingresamos al laboratorio de XSS Reflejado e insertamos el siguiente payload:

```html
<h1>Prueba insertar html</h1>
```

El contenido HTML se ejecuta correctamente, confirmando que el sitio refleja el input del usuario sin filtrado.

![Web](Imágenes/Capturas_6.png)

---

![Maquina1](Imágenes/Capturas_5.png)

## 🧪 **XSS Almacenado**

Probamos el siguiente payload:

```html
<p style="color:blue;">Azul</p>
```

Este se muestra correctamente en azul porque solo contiene HTML y CSS. Sin embargo, payloads como:

```html
<script>alert('XSS')</script>
```

no se ejecutan visualmente, aunque sí se almacenan. Esto puede deberse a políticas del navegador o mecanismos de seguridad activos.

También funciona el siguiente ejemplo de tipo evento:

```html
<div onmouseover="alert('XSS')">Pasa el mouse</div>
```

![Maquina2](Imágenes/2025-05-19_10-13.png)

---

## 🧪 **XSS en Dropdowns**

Payload usado en los parámetros de la URL:

```
http://172.17.0.3/laboratorio3/?opcion1=%3C/p%3E%3Ch1%3EAlejandroSL%3C/h1%3E%3Cp%3E&opcion2=%3C/p%3E%3Cp%3EEsta%20es%20otra%20opcion%3C/p%3E%3Cp%3E&opcion3=%3C/p%3E%3Cp%3E%3Cb%3EVulnerado%3C/b%3E%3C/p%3E
```

Esto funciona porque el contenido de los parámetros se inserta directamente en el HTML sin sanitización. Al cerrar etiquetas (`</p>`) y agregar nuevas (`<h1>`, `<b>`), se rompe la estructura original y se reemplaza por el contenido personalizado.

![Maquina3](Imágenes/Capturas_7.png)

---

## 🧪 **XSS basado en Parámetros GET**

Se utiliza el siguiente payload:

```
http://172.17.0.3/laboratorio4/?data=<div onmouseover="alert('XSS')">Pasa el mouse</div>
```

Este ejemplo demuestra que la página refleja directamente el valor del parámetro `data` sin ningún filtrado, permitiendo la ejecución de JavaScript. Al pasar el cursor sobre el texto, se activa una alerta.

![Maquina4](Imágenes/Capturas_8.png)

---

## 🔐 **Obtención de Credenciales y Acceso SSH**

En el código fuente del sitio, se observan las credenciales para acceder por SSH:

* **Usuario:** `balu`
* **Contraseña:** `balulero`

---

## 🚀 **Escalada de Privilegios**

Una vez dentro como `balu`, se descubre un archivo `secret.bak` que contiene:

```
balulito:balulerochingon
```

Con estas credenciales, accedemos como `balulito` y ejecutamos `sudo -l`, que indica que este usuario puede ejecutar `cp` como root sin contraseña. Aprovechamos esto para copiar un archivo modificado `/tmp/passwdroot` sobre `/etc/passwd`. En el archivo modificado, se elimina la `x` del usuario root, haciendo que no requiera contraseña. Luego se accede con `su root` y se obtiene acceso completo al sistema.

![root ](Imágenes/Capturas_10.png)

---

