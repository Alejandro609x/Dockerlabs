# 🧠 **Informe de Pentesting – Máquina: Bicho**

### 💡 **Dificultad:** Fácil

![Despliegue](Imágenes/2025-05-20_04-42.png)

---

## 📝 **Descripción de la máquina**


---

## 🎯 **Objetivo**

---

## ⚙️ **Despliegue de la máquina**

Se descarga el archivo comprimido de la máquina vulnerable y se lanza el contenedor Docker mediante el script incluido:

```bash
unzip bicho.zip
sudo bash auto_deploy.sh backend.tar
```

![Despliegue](Imágenes/Capturas.png)

---

## 📡 **Comprobación de conectividad**

Verificamos que la máquina se encuentra activa respondiendo a peticiones ICMP (ping):

```bash
ping -c1 172.17.0.2
```

![Ping](Imágenes/Capturas_1.png)

---

## 🔍 **Escaneo de Puertos**

Realizamos un escaneo completo para detectar todos los puertos abiertos:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts.txt
```

**Puertos detectados:**

* `22/tcp`: SSH
* `80/tcp`: HTTP

![Puertos](Imágenes/Capturas_2.png)

Luego, analizamos los servicios y versiones asociados a esos puertos:

```bash
nmap -sCV -p22,80 172.17.0.2 -oN target.txt
```

![Servicios](Imágenes/Capturas_3.png)

---

En el escaeno se encontro un dombre de dominio y lo agregamo a nano /etc/hosts 172.17.0.2 bicho.dl
![etc/host](Imágenes/Capturas_4.png)

---
Al entrar http://172.17.0.2 encontramos una pagina de bienbenida
![Pagina](Imágenes/Capturas_5.png)

Al solo tener disponible una pagina web busque mas inforamcion al realizar fuzzin no se encontro nada pero use whatweb '172.17.0.2' y encontre que trabaja con WordPress y al buscar alguna vulnerabilidad con searchsploit WordPress 6.6.2 encontre que puede 
ser vulnerable a InyeccionSQL
![Versiones](Imágenes/Capturas_6.png)

Use wpscan --url http://bicho.dl/ --enumerate u para escanear el sitio WordPress y descubrir los nombres de usuario registrados en este caso se encotro el usuario bicho.
![wpscan](Imágenes/Capturas_7.png)

hicimos un fuzzin a gobuster dir -u  http://bicho.dl/wp-content/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20 -add-slash -b 403,404 -x .php,.html,.txt el directorio /wp-content/ se encontro en la busqueda de usuario 
anteriror y se encontraron:
/index.php           
/themes               
/uploads             
/plugins         
/upgrade            
/fonts                
![Fuzzing](Imágenes/Capturas_8.png)




