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

