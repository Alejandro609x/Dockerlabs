# 🖥️ **Máquina: Backend**  
- **🔹 Dificultad:** Fácil  
- **📌 Descripción:**  
  Esta máquina de DockerLabs pone a prueba habilidades en la explotación de bases de datos mediante **inyecciones SQL (SQLi)**. Se enfoca en la identificación y explotación de vulnerabilidades en consultas MySQL, lo que permite el acceso no autorizado a la base de datos y la extracción de información sensible.  

- **🎯 Objetivo:**  
  - Identificar y explotar fallos de seguridad en la aplicación backend mediante técnicas de **inyección SQL**.  
  - Comprender su impacto.  

![Máquina Backend](/Backend/Images/Maquina.png)

---

## 🚀 **Iniciando la Máquina Backend en DockerLabs**  

Para desplegar la máquina, sigue estos pasos:  

### 1️⃣ **Descargar y descomprimir el archivo**  
Primero, descarga el archivo `.zip` y extráelo. En mi caso, uso `7z`:  

```bash
7z e backend.zip
```

### 2️⃣ **Ejecutar el despliegue automático**  
Una vez descomprimido, ejecuta el siguiente comando para desplegar la máquina:  

```bash
bash auto_deploy.sh backend.tar
```

---

📌 **Nota:** Asegúrate de tener `7z` instalado y de ejecutar el script en un entorno adecuado con Docker configurado.  

![Máquina Iniciada](/Backend/Images/inicio.jpeg)

Una vez iniciada compruebas la conecion y con el comando:
```bash
ping -c4 172.17.0.2
```
Una vez confirmada la conexion comenzamos con las fase de reconocimiento usando el comando:
```bash
nmap -p- --open -sS --min-rate 500 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```
📌 **Nota:** En mis repositorios puedes encontrar información sobre los comandos empleados en esta fase ya que uso script personalizados.

Extraigo la informacion importante con el comando personalizado:
```bash
extracPorts allPorts.txt
```
![Reconocimiento](/Backend/Images/escaneo.jpeg)

Con las informacion estraida hacemos un reconocimeto mas exahustivo con los puertos que ya conocemos y ver las información sobre los servicios que corren en los puertos, para esto usamos el comando:
```bash
nmap -p22,80 -sCV 172.17.0.2 -oN target
```
📌 **Nota:** Con esta informacón podemos empezar a busacr vulberabilidades por las verciones que nos muestras y ver los servicios y como podiramos atacar, en este caso el puerto 22 corresponde al SSH y el puertp 80 nos muestra que en ese puerto corre una pagina web.

![Reconocimiento](/Backend/Images/puertos.jpeg)

Para que el navegador nos muestre la pagina web tenemos que meter la dirección IP de la maquina 172.17.0.2, podemos abrir el archivo con:
```bash
nano /etc/hosts
```
![directorio](/Backend/Images/etchost.jpeg)

Podemos recopilar información sobre la pagina web con, esto es util para ver sobre los servicios que trabaja y la verciones de la pagina y poder encontrar una vulnerabilidad:
```bash
whatweb 172.17.0.2
```
![Reconocimiento](/Backend/Images/whatweb.jpeg)

Ya que sabemos que estamos trabajando una pagina web podemos ver que tiene un apartado de login, intentamos entrar con credenciales de podria venir pordefecto y con este verificamos si podriamos entrar, pero no tiene estas credenciales habilitadas.

![pagina](/Backend/Images/pruebas.jpeg)

Hacemos uso de gobuster para buscar directorios:
```bash
gobuster dir -u /usr/share/seclists/Discovery/web-Content/directory-list-2.3-medium.txt -t 20 -add-slash -b '403,404 -x php,html,txt
```
📌 **Nota:** -u sirve para definir una biblioteca de directorios si no la tienes instalada puedes usar apt install, ademas podriamos usar gobuster para buscar sub-dominios pero cuando realice la practica deduje que seria una ataque por inyeccioón MySQL, solo me llamo la atencion que la url aparecia como index.html y login.html y queria probar si podria existir mas directorios ocultos y no huvo directorios impoertantes.
```bash
apt -y install seclists
```

![directorios](/Backend/Images/directorios.jpeg)

Para confirmas si era vulnerable la pagina una inyección use admin' en un campo de usuario y la aplicación respondio con un error de base de datos, y esto confirma que el sitio es vulnerable a inyecciones SQL. Esto sucede porque el carácter de comilla simple (') puede alterar la estructura de la consulta SQL.

![pagina](/Backend/Images/pagina.jpeg)

![error](/Backend/Images/sql.jpeg)

Hice uso de Burp Suite para poder mandar la peticion a mi proxy y copiar la peticion un archivo .req para poder usarlo posteriormente.

![peticiones](/Backend/Images/peticion.jpeg)

Con la herramineta sqlmap que sirve para realizar inyecciones sql automaticamente la use para realizar ataques al formulario y poder optener informacion sensible.
```bash
sqlmap -r peticiones.req --level=5 --risk=3 --dump 
```
![sql](/Backend/Images/sqlmap.jpeg)

Una vez que te se termino la inyeccion podemo soptener una base de datos llamada users con usuarios y contraseñas, estas credenciales no tuvieron exito en el inicio de sesión en la pagina web y se intentento acceder por SSH el cual la unica credencial valida fue pepe, al ser pocas contraseñas se hizo manual pero se puede realizar por la herramineta hydra.
Nos conectapor por SSH:
```bash
ssh pepe@172.17.0.2 -p 22
```
![ssh](/Backend/Images/conectarssh.jpeg)

📌 **Nota:** Esta herramienta esta penalizada en las certificaciones y en esta las tienes que realizar manualmente.

Se buscan vulnerabilidades para poder escalar privilegios en donde este comando nos mostro que podemos ejecutar comados grep y ls con privilegios de root y pudimos conseguir un hash MD5 (con la practica puedes identificar los tipos). 
```bash
find / \-perm -4000 2>/dev/null
```
![buscar](/Backend/Images/Buscar.jpeg)

Guardamos el hash como .txt y con la herramienta John the ripper podemos podemos conseguir la contraseña con el cual nos sirve para conectarnos a SSH como root.
![contraseña](/Backend/Images/ContraseñaRoot.jpeg)

📌 **Nota:** Puedes hacerlo directamente con comados bash o con paginas de internet.

