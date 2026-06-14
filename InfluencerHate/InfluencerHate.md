# 🧠 **Informe de Pentesting – Máquina: InfluencerHate**

### 💡 **Dificultad:** Fácil

📦 **Plataforma:** DockerLabs

![Despliegue](Imagenes/logo.png)
---

# 🚀 **Despliegue de la Máquina**

Para iniciar la máquina vulnerable, primero descomprimimos el archivo proporcionado y posteriormente ejecutamos el script de despliegue:

```bash
unzip influencerhate.zip
sudo bash auto_deploy.sh influencerhate.tar
```

![Despliegue](Imagenes/despliegue.png)

---

# 📶 **Comprobación de Conectividad**

Una vez desplegada la máquina, verificamos que el objetivo se encuentre activo y responda correctamente a peticiones ICMP:

```bash 
ping -c1 172.17.0.2
```

Esto nos permite confirmar que la máquina está encendida y accesible dentro de la red local del laboratorio.

![Despliegue](Imagenes/ping.png)

---

# 🔍 **Escaneo de Puertos**

## 🔎 Escaneo Completo de Puertos

Se realiza un escaneo completo sobre todos los puertos TCP para identificar los servicios expuestos en la máquina víctima:

```bash 
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2
```

### 📌 Puertos Abiertos Detectados

* `22/tcp` → Servicio SSH
* `80/tcp` → Servicio HTTP 

![Despliegue](Imagenes/nmapuno.png)
---

## 🧩 Enumeración de Servicios y Versiones

Después de identificar los puertos abiertos, procedemos a detectar versiones y configuraciones de los servicios activos:

```bash 
nmap -sCV -p22,80,3306 172.17.0.2
```

Este análisis permite obtener información más detallada sobre los servicios en ejecución, versiones instaladas y posibles configuraciones vulnerables.

![Despliegue](Imagenes/nmapdos.png)

---

Al saber que existe el servicio http por el puerto 80 entramos a revisar la pagina y nos muetsra un formualario de inicio de sesion

![Despliegue](Imagenes/nmapdos.png)

Se realizo fuzzing y diversos ataque sin exito, posterior se introdujo credenciales admin:admin para interceptar la peticiòn con la herramineta burtsuite y poder analizar el GET.

![Despliegue](Imagenes/Burtsuite.png)

Al analizar "YWRtaW46YWRtaW4=" resultado de la peticiòn peticioòn se descubre que esta trabajando con Basic: en Base65, se confirma gracias a:

```bash 
echo 'YWRtaW46YWRtaW4=' | base64 -d
```

![Despliegue](Imagenes/base64.png)

Obtenenos admin:admin las credenciales antes introducidas.

Se procede a realizar fuerza bruta con el directorio: Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt
Pagina de SecLists: https://github.com/danielmiessler/SecLists/blob/master/Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt

```bash 
hydra -C ftp-credenciales.txt 172.17.0.2 http-get / -t 64 -I -e nsr
```
![Despliegue](Imagenes/hydra.png) 

Y obtendremos las credenciales: httpadmin:fhttpadmin con estas podemos acceder al primer formulario de login.

Al acededer nos muestra la siguiente pagina: 

![Despliegue](Imagenes/paginados.png) 

Y al realizar nuevamente el fuzzing:

```bash
gobuster dir -u http://172.17.0.2/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x .env,.php,.bak,.old,.zip,.txt -b 403,303,404 --exclude-length 457 -H "Authorization: Basic aHR0cGFkbWluOmZodHRwYWRtaW4="
```
Pero agrenando el paramero -H (Explica esta parte del parametro), obtendermos el directorio:

/login.php

![Despliegue](Imagenes/gobuster.png) 

Al acceder a la pagina encontramos un nuevo formulario de login.

![Despliegue](Imagenes/paginatres.png) 



