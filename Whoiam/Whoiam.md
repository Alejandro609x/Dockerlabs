## Informe de Pentesting: Máquina Vulnerable "Whoiam"

### Descripción General:

La máquina vulnerable "Whoiam" es una máquina de DockerLabs diseñada para practicar técnicas de pentesting. El objetivo es realizar un análisis exhaustivo, comenzando desde la verificación de la conexión hasta la escalada de privilegios a root, para identificar vulnerabilidades y explotar los servicios disponibles.

### Paso 1: Despliegue de la Máquina

**Comando ejecutado:**

```bash
unzip whoiam.zip
./auto_deploy.sh whoiam.tar
```

Una vez descargado el archivo comprimido `.zip` desde la página de DockerLabs, se descomprimió utilizando el comando `unzip whoiam.zip`. Posteriormente, se desplegó la máquina utilizando el script `auto_deploy.sh` junto con el archivo `whoiam.tar`.

### Paso 2: Verificación de Conexión

**Comando ejecutado:**

```bash
ping -c1 172.18.0.2
```

Se realizó un `ping` a la dirección IP de la máquina víctima, `172.18.0.2`, para verificar que la máquina estuviera activa y accesible en la red.

![Imagen 2](Whoiam/Imagenes/Dos.jpeg)

### Paso 3: Escaneo de Puertos con Nmap

**Comando ejecutado:**

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.18.0.2 -oG allPorts.txt
```

Con `nmap` se realizó un escaneo de puertos completo para identificar puertos abiertos en la máquina. Se encontró que solo el puerto 80 (HTTP) estaba abierto, lo que sugiere que podría haber una página web disponible.

**Comando adicional:**

```bash
nmap -p22,21 172.18.0.2
```

Se verificó que los puertos de los servicios SSH (22) y FTP (21) no estaban abiertos, lo que confirmaba que no eran accesibles desde la máquina.

![Imagen 3](Whoiam/Imagenes/Tres.jpeg)

### Paso 4: Extracción de Puertos Importantes

**Comando ejecutado:**

```bash
extractPorts allPorts.txt
nmap -sC -sV -p 80 172.18.0.2 -oN target.txt
```

Se extrajeron los puertos importantes del archivo de salida de `nmap` utilizando la herramienta `extractPorts`. Luego, se volvió a escanear el puerto 80 para obtener información adicional sobre el servicio y sus versiones.

![Imagen 4](Whoiam/Imagenes/Cuatro.jpeg)

### Paso 5: Investigación de la Página Web

**URL visitada:**

```http
http://172.18.0.2
```

Se accedió a la página web disponible en el puerto 80, pero no se encontró información relevante de inmediato. Por lo tanto, se decidió realizar un fuzzing en busca de directorios ocultos.

![Imagen 5](Whoiam/Imagenes/Cinco.jpeg)

### Paso 6: Fuzzing de Directorios con Gobuster

**Comando ejecutado:**

```bash
gobuster dir -u http://172.18.0.2/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20 -add-slash -b 403,404 -x php,html,txt
```

Se utilizó `gobuster` para buscar directorios ocultos en la página web. Durante la investigación de los directorios encontrados, se identificaron varios archivos relacionados con WordPress, como registros de inicio de sesión y archivos de configuración. Además, se encontró un directorio que contenía una base de datos.

![Imagen 6](Whoiam/Imagenes/Seis.jpeg)

### Paso 7: Análisis de la Base de Datos

**Comando ejecutado:**

```bash
unzip databaseback2may.zip
```

El archivo comprimido `databaseback2may.zip` fue descomprimido, y se abrió el archivo `29DBMay`, que contenía credenciales que probablemente podrían usarse para acceder al servicio de WordPress.

![Imagen 7](Whoiam/Imagenes/Siete.jpeg)

### Paso 8: Acceso a WordPress

Con las credenciales descubiertas (`Username: developer`, `Password: 2wmy3KrGDRD%RsA7Ty5n71L^`), se logró iniciar sesión en el servicio de WordPress.

![Imagen 8](Whoiam/Imagenes/Ocho.jpeg)

### Paso 9: Carga de un Web Shell

Se creó un archivo PHP malicioso llamado `revellshell.php` para abrir una terminal inversa. El archivo fue comprimido en un archivo `.zip` ya que la página solo aceptaba este tipo de archivos.

**Comando ejecutado:**

```bash
nano revellshell.php
7z a revellshell.zip revellshell.php
```

![Imagen 9](Whoiam/Imagenes/Nueve.jpeg)

### Paso 10: Configuración de Escucha

Se configuró un puerto para escuchar conexiones entrantes, en este caso, el puerto 443.

![Imagen 10](Whoiam/Imagenes/Once.jpeg)

### Paso 11: Carga del Web Shell en WordPress

El archivo comprimido con el web shell se cargó a través del panel de administración de WordPress, utilizando la opción "Add New Plugin".

![Imagen 11](Whoiam/Imagenes/Doce.jpeg)

### Paso 12: Ejecución del Web Shell

Una vez cargado y activado el plugin, se logró obtener una terminal inversa que permitió ejecutar comandos en la máquina víctima.

![Imagen 12](Whoiam/Imagenes/Trece.jpeg)

### Paso 13: Escalada de Privilegios

Se ejecutaron los siguientes comandos para escalar privilegios:

**Comando para revisar sudoers:**

```bash
sudo -l
```

Se verificó la configuración de `sudo` y se encontró que el usuario podía ejecutar ciertos comandos como otros usuarios. Utilizando esto, se logró ejecutar un comando para obtener acceso al sistema con privilegios elevados.

**Comando ejecutado:**

```bash
sudo -u rafa /usr/bin/find . -exec /bin/bash \;
```

Se utilizó el comando `find` con `sudo` para ejecutar un shell interactivo.

![Imagen 13](Whoiam/Imagenes/Catorce.jpeg)

Después, se ejecutó un comando más con el usuario `ruben` para obtener acceso a otras áreas del sistema.

**Comando ejecutado:**

```bash
sudo -u ruben /usr/sbin/debugfs
```

Finalmente, se accedió a un script en el directorio `/opt/`, que se ejecutó con privilegios elevados.

**Comando ejecutado:**

```bash
sudo /bin/bash /opt/pinguin.sh
```

Con estos pasos, se logró escalar los privilegios y obtener acceso completo como root.

![Imagen 14](Whoiam/Imagenes/Diecisiete.jpeg)

### Conclusión:

Este informe detalla el proceso completo de penetración de la máquina vulnerable "Whoiam", desde la verificación de la conexión hasta la escalada de privilegios a root. Cada paso fue cuidadosamente documentado y acompañado de imágenes que ilustran las acciones realizadas. El uso de herramientas como `nmap`, `gobuster`, y la explotación de configuraciones de `sudo` fueron clave para lograr el acceso a nivel de root.
