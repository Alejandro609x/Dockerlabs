# 🖥️ **Máquina: Backend**  
- **🔹 Dificultad:** Fácil  
- **📌 Descripción:**  
  Esta máquina de DockerLabs está diseñada para poner a prueba habilidades en la explotación de bases de datos mediante **inyecciones SQL (SQLi)**. Se centra en la identificación y explotación de vulnerabilidades en consultas MySQL, lo que permite obtener acceso no autorizado a la base de datos y extraer información sensible.  

- **🎯 Objetivo:**  
  - Identificar y explotar fallos de seguridad en la aplicación backend mediante técnicas de **inyección SQL**.  
  - Comprender el impacto de estas vulnerabilidades.  

![Máquina Backend](/Backend/Images/Maquina.png)

---

## 🚀 **Despliegue de la Máquina Backend en DockerLabs**  

Para iniciar la máquina, sigue estos pasos:

### 1️⃣ **Descargar y descomprimir el archivo**  
Comienza descargando el archivo `.zip` y extráelo. En mi caso, utilizo `7z`:

```bash
7z e backend.zip
```

### 2️⃣ **Ejecutar el despliegue automático**  
Una vez descomprimido el archivo, ejecuta el siguiente comando para desplegar la máquina:

```bash
bash auto_deploy.sh backend.tar
```

---

📌 **Nota:** Asegúrate de tener `7z` instalado y de ejecutar el script en un entorno adecuado con Docker configurado.  

![Máquina Iniciada](/Backend/Images/inicio.jpeg)

Una vez iniciada, comprueba la conexión con el siguiente comando:

```bash
ping -c4 172.17.0.2
```

Cuando la conexión esté confirmada, comenzamos la fase de reconocimiento con:

```bash
nmap -p- --open -sS --min-rate 500 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

📌 **Nota:** En mis repositorios encontrarás scripts personalizados con los comandos utilizados en esta fase.

Para extraer la información relevante de los resultados de escaneo, utilizo el siguiente comando:

```bash
extracPorts allPorts.txt
```

![Reconocimiento](/Backend/Images/escaneo.jpeg)

Con los puertos identificados, realizamos un análisis más detallado con el siguiente comando para obtener información sobre los servicios que están corriendo en dichos puertos:

```bash
nmap -p22,80 -sCV 172.17.0.2 -oN target
```

📌 **Nota:** Esta información nos permite identificar posibles vulnerabilidades basadas en las versiones de los servicios, como en este caso, donde el puerto 22 está relacionado con SSH y el puerto 80 con una página web.

![Reconocimiento](/Backend/Images/puertos.jpeg)

Para acceder a la página web desde el navegador, añade la dirección IP de la máquina (172.17.0.2) en tu archivo de hosts. Para ello, edita el archivo con:

```bash
nano /etc/hosts
```

![directorio](/Backend/Images/etchost.jpeg)

Luego, recopilamos información sobre la página web con el siguiente comando, lo que nos permitirá conocer los servicios y versiones utilizados, y buscar posibles vulnerabilidades:

```bash
whatweb 172.17.0.2
```

![Reconocimiento](/Backend/Images/whatweb.jpeg)

Al acceder a la página, observamos que existe un formulario de login. Intentamos ingresar utilizando credenciales predeterminadas, pero no tienen éxito.

![pagina](/Backend/Images/pruebas.jpeg)

Para encontrar posibles directorios ocultos, utilizamos **gobuster** con una lista de directorios conocida:

```bash
gobuster dir -u /usr/share/seclists/Discovery/web-Content/directory-list-2.3-medium.txt -t 20 -add-slash -b '403,404' -x php,html,txt
```

📌 **Nota:** Si no tienes instalada la lista de directorios, puedes hacerlo con:

```bash
apt -y install seclists
```

Aunque no encontramos directorios importantes, el uso de **gobuster** también podría haber sido útil para buscar subdominios. Sin embargo, en este caso, deduje que el ataque sería por inyección MySQL, dado que la URL mostraba como `index.html` y `login.html`.

![directorios](/Backend/Images/directorios.jpeg)

Para confirmar si la página es vulnerable a inyecciones SQL, intentamos ingresar `admin'` en el campo de usuario, lo que provoca un error de base de datos. Esto indica que la página es vulnerable a inyecciones SQL, ya que el carácter de comilla simple (') altera la estructura de la consulta SQL.

![pagina](/Backend/Images/pagina.jpeg)

![error](/Backend/Images/sql.jpeg)

Utilizamos **Burp Suite** para interceptar la solicitud y luego copiarla a un archivo `.req`, lo que nos permitirá usarla más tarde.

![peticiones](/Backend/Images/peticion.jpeg)

Con **sqlmap**, una herramienta automática para realizar inyecciones SQL, atacamos el formulario para obtener información sensible. El comando utilizado fue:

```bash
sqlmap -r peticiones.req --level=5 --risk=3 --dump
```

![sql](/Backend/Images/sqlmap.jpeg)

Al finalizar la inyección, conseguimos acceder a una base de datos llamada **users**, que contiene nombres de usuario y contraseñas. Sin embargo, estas credenciales no fueron válidas para iniciar sesión en la página web. Intentamos acceder por SSH y encontramos que la única credencial válida era `pepe`. Aunque se intentó hacer un ataque automatizado con **Hydra**, la cantidad de contraseñas era pequeña, por lo que se optó por hacerlo manualmente.

Para acceder por SSH, usamos:

```bash
ssh pepe@172.17.0.2 -p 22
```

![ssh](/Backend/Images/conectarssh.jpeg)

📌 **Nota:** En este caso, el uso de herramientas automatizadas como **Hydra** no es recomendable para certificaciones, ya que debes realizar el ataque de forma manual.

Una vez dentro, buscamos posibles vulnerabilidades para escalar privilegios. Al ejecutar el siguiente comando, descubrimos que podíamos ejecutar **grep** y **ls** con privilegios de root, lo que nos permitió obtener un hash MD5.

```bash
find / -perm -4000 2>/dev/null
```

![buscar](/Backend/Images/Buscar.jpeg)

Guardamos el hash en un archivo de texto y utilizamos **John the Ripper** para descifrarlo. Con la contraseña obtenida, conseguimos acceder a SSH como root.

![contraseña](/Backend/Images/ContraseñaRoot.jpeg)

📌 **Nota:** También puedes realizar este proceso directamente con comandos bash o utilizar páginas web especializadas para descifrar hashes.


