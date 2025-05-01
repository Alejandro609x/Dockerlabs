# 🖥️ Máquina: Injection  
**Nivel:** Muy fácil  
**Objetivo:** Obtener acceso como usuario `root` mediante explotación de vulnerabilidades web y escalada de privilegios en el sistema.

---

## 🧩 Descripción

Se trata de una máquina vulnerable con una aplicación web que permite realizar una inyección SQL. El objetivo es identificar los servicios expuestos, explotar la vulnerabilidad, obtener acceso como usuario del sistema y escalar privilegios a `root`.

---

## 🛠️ Despliegue

![](/Injection/Imagenes/Logo.png)

Primero, descargamos el archivo comprimido con la máquina desde DockerLabs. Posteriormente lo descomprimimos y lo desplegamos en el entorno local utilizando los siguientes comandos:

```bash
unzip trust.zip
sudo bash auto_deploy.sh injection.tar
```

![](/Injection/Imagenes/Inicio.jpeg)

---

## 🔎 Verificación de conectividad

Se verifica que la máquina se encuentra activa realizando un `ping` a su dirección IP:

```bash
ping -c4 172.17.0.2
```

![](/Injection/Imagenes/Ping.jpeg)

---

## 🔍 Enumeración de puertos

Se realiza un escaneo de todos los puertos (`-p-`) con `nmap`, utilizando TCP SYN scan (`-sS`) y velocidad aumentada (`--min-rate 5000`):

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

Se detectan los siguientes puertos abiertos:
- **22**: SSH
- **80**: HTTP

![](/Injection/Imagenes/Puertos.jpeg)

Se realiza un segundo escaneo más detallado en los puertos detectados:

```bash
nmap -sC -sV -p 22,80 172.17.0.2 -oN target.txt
```

Este escaneo utiliza scripts por defecto (`-sC`) y detección de versiones (`-sV`) para identificar servicios y posibles vulnerabilidades asociadas.

![](/Injection/Imagenes/Servicios.jpeg)

---

## 🌐 Análisis web manual

Al acceder al sitio web en el puerto 80 desde el navegador, se visualiza un formulario de inicio de sesión.

![](/Injection/Imagenes/Pagina.jpeg)

Como prueba inicial, se introduce un carácter de comilla simple `'` en uno de los campos del formulario. La aplicación devuelve un error, lo cual indica que probablemente esté concatenando directamente la entrada del usuario en una consulta SQL sin sanitización, mostrando **posible vulnerabilidad a inyección SQL**.

---

## 🧪 Interceptación con Burp Suite y explotación con SQLMap

La solicitud del formulario se intercepta mediante Burp Suite. Se guarda la petición HTTP en un archivo `.req` para su análisis automatizado:

![](/Injection/Imagenes/Burp.jpeg)

Luego se ejecuta `sqlmap` sobre dicha petición con opciones elevadas de detección:

```bash
sqlmap -r peticiones.req --level=5 --risk=3 --dump
```

- `-r`: especifica el archivo con la petición HTTP.
- `--level=5` y `--risk=3`: aumentan la agresividad y profundidad de las pruebas.
- `--dump`: indica que se desea extraer el contenido de las bases de datos vulnerables.

Como resultado, se obtiene una tabla con **nombres de usuario y contraseñas**.

![](/Injection/Imagenes/usuarios.jpeg)

---

## 🔐 Acceso al sistema por SSH

Con las credenciales obtenidas, se intenta acceder al sistema mediante SSH:

```bash
ssh dylan@172.17.0.2
```

El acceso es exitoso, lo que confirma que la base de datos contenía credenciales válidas para un usuario del sistema.

---

## ⬆️ Escalada de privilegios

Se busca ejecutar procesos como `root` que estén configurados con el bit SUID habilitado, lo cual permite que se ejecuten con privilegios elevados independientemente del usuario que los ejecute:

```bash
find / -perm -4000 -user root 2>/dev/null
```

Entre los binarios listados se encuentra:

```
/usr/bin/env
```

Este binario es relevante porque permite ejecutar un comando o script dentro de un entorno modificado. Cuando está marcado con el bit SUID y pertenece a `root`, se puede abusar para ejecutar una shell como `root`.

### ¿Por qué `/usr/bin/env` es útil?

El binario `env` puede ser usado para invocar un intérprete de comandos (`/bin/sh`) con privilegios elevados, debido a que:

- Tiene el bit **SUID** activo.
- Permite la ejecución de binarios arbitrarios bajo el entorno actual.
- No requiere argumentos especiales ni validación adicional.

Si el sistema no restringe esta ejecución (por ejemplo, mediante `noexec` o `secure_path`), se puede obtener una shell con privilegios de root usando:

```bash
/usr/bin/env /bin/sh -p
```

- La opción `-p` preserva los privilegios efectivos del ejecutable padre (en este caso, `root`), lo que resulta en una shell con permisos de superusuario.

Ejecución:

```bash
dylan@2bb2e0218567:/$ /usr/bin/env /bin/sh -p
# whoami
root
# exit
```

![](/Injection/Imagenes/SSh.jpeg)

---

## ✅ Conclusión

Se logró el objetivo de comprometer el sistema y obtener acceso como `root`. El proceso incluyó:

1. Enumeración de puertos expuestos (22 y 80).
2. Detección de una vulnerabilidad de inyección SQL en un formulario web.
3. Explotación de la vulnerabilidad para extraer credenciales válidas.
4. Acceso al sistema mediante SSH con dichas credenciales.
5. Escalada de privilegios abusando del binario `/usr/bin/env` con SUID activo para ejecutar una shell como `root`.

Este ejercicio demuestra la importancia de validar correctamente las entradas del usuario, así como limitar el uso de binarios con SUID innecesarios en sistemas productivos.

---

> ⚠️ **Nota:** En ciertas certificaciones como **OSCP**, **OSWE**, o entornos de evaluación restringidos, el uso de herramientas automatizadas como **Burp Suite Intruder** o **SQLMap** puede estar **estrictamente prohibido**. Estas herramientas simplifican la explotación, pero pueden ir en contra de los principios de aprendizaje, análisis manual o evaluación ética establecidos por la organización. Asegúrate siempre de revisar las políticas antes de usarlas.
