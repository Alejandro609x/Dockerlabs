# 🧠 **Informe de Pentesting – Máquina: Extraviado**

### 💡 **Dificultad:** Fácil

---

### 🕵️‍♂️ **Tipo de ataque:**

**Acceso SSH mediante credenciales expuestas en Base64, enumeración de usuarios y lectura de archivos ocultos con pistas para escalada de privilegios.**

![Despliegue](Imágenes/2025-05-19_15-52.png)

---

## 📝 **Descripción de la máquina**

Extraviado es una máquina vulnerable de dificultad baja, ideal para familiarizarse con la decodificación de datos ocultos, la enumeración básica de usuarios y la búsqueda de archivos ocultos como medio para la escalada de privilegios.

---

## 🎯 **Objetivo**

Obtener acceso como **root** dentro del sistema objetivo mediante análisis de puertos, descubrimiento de credenciales y explotación de archivos ocultos con pistas.

---

## ⚙️ **Despliegue de la máquina**

Se descarga y despliega la máquina utilizando el script automatizado provisto:

```bash
unzip extraviado.zip
sudo bash auto_deploy.sh extraviado.tar
```

![Despliegue](Imágenes/Capturas.png)

---

## 📡 **Comprobación de conectividad**

Verificamos que el contenedor está activo mediante una solicitud `ping`:

```bash
ping -c1 172.17.0.3
```

![Ping](Imágenes/Capturas_1.png)

---

## 🔍 **Escaneo de Puertos**

Realizamos un escaneo completo para identificar los puertos abiertos:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.3 -oG allPorts.txt
```

**Puertos detectados:**

* `22/tcp`: SSH
* `80/tcp`: HTTP

![Puertos](Imágenes/Capturas_2.png)

Posteriormente, enumeramos servicios y versiones:

```bash
nmap -sCV -p22,80 172.17.0.3 -oN target.txt
```

![Servicios](Imágenes/Capturas_3.png)

---

## 🌐 **Análisis del servicio web (HTTP)**

Al acceder al sitio en `http://172.17.0.3`, se muestra la página por defecto de Apache.

![Pagina](Imágenes/Capturas_4.png)

Sin embargo, al inspeccionar el código fuente, se encuentran dos cadenas sospechosas codificadas en **Base64**:

* `ZGFuaWVsYQ==`
* `Zm9jYXJvamE=`

![Fuente](Imágenes/Capturas_5.png)

Las descodificamos con el comando:

```bash
echo 'ZGFuaWVsYQ==' | base64 --decode
daniela%

echo 'Zm9jYXJvamE=' | base64 --decode
focaroja%
```

![Descodificar](Imágenes/Capturas_6.png)

---

## 🔐 **Acceso mediante SSH**

Con las credenciales obtenidas:

* **Usuario:** daniela
* **Contraseña:** focaroja

Accedemos al sistema vía SSH. Luego, al intentar `sudo -l`, no se tienen permisos administrativos.

Explorando el sistema, descubrimos otro usuario: `diego`.

---

## 📁 **Enumeración de archivos ocultos**

Dentro del directorio `/home/daniela`, encontramos un directorio oculto `.secreto` que contiene el archivo `.passdiego`. Este archivo posee otra cadena en Base64:

```bash
echo 'YmFsbGVuYW5lZ3Jh' | base64 --decode
ballenanegra%
```

Con esto, accedemos como `diego`:

```bash
su diego
```

---

## 📦 **Escalada de privilegios – búsqueda de root**

En `/home/diego`, encontramos otro archivo oculto: `.passroot/.pass`, que al ser decodificado muestra:

```bash
echo 'YWNhdGFtcG9jb2VzdGE=' | base64 --decode
acatampocoesta%
```

Sin embargo, esta contraseña no permite escalar a root.

---

## 🔍 **Hallazgo clave en archivos compartidos**

Al buscar en:

```bash
cd /home/diego/.local/share
```

Encontramos un archivo sin nombre aparente (`cat .-`) que contiene un **acertijo**:

> En un mundo de hielo, me muevo sin prisa,
> con un pelaje que brilla, como la brisa.
> No soy un rey, pero en cuentos soy fiel,
> de un color inusual, como el cielo y el mar también.
> Soy amigo de los niños, en historias de ensueño.
> ¿Quién soy, que en el frío encuentro mi dueño?

La solución al acertijo es:

### ✅ **osoazul**

Explicación: describe a un animal ficticio, amigable, peludo, de ambiente frío y asociado a cuentos infantiles.

---

## 👑 **Acceso a root**

Usamos la contraseña `osoazul` para convertirnos en root:

```bash
su root
```

![root](Imágenes/Capturas_7.png)

---

## 🏁 **Conclusión**

La máquina **Extraviado** expone una cadena lógica de vulnerabilidades y pistas en texto plano codificado en Base64. Desde credenciales básicas hasta un acertijo final para obtener acceso completo como `root`, la máquina pone a prueba habilidades esenciales como:

* Enumeración web
* Decodificación
* Exploración de archivos ocultos
* Pensamiento lateral en resolución de acertijos

---
