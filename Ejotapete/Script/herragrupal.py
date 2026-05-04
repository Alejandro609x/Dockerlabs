#!/usr/bin/env python3
import re
from urllib.parse import urlparse

def parse_target(target):
    # Si no tiene esquema, lo añadimos
    if not re.match(r'http[s]?://', target):
        target = 'http://' + target

    parsed = urlparse(target)

    scheme = parsed.scheme
    host = parsed.hostname
    port = parsed.port
    path = parsed.path if parsed.path else "/"

    # Puerto por defecto
    if port is None:
        if scheme == "https":
            port = 443
        else:
            port = 80

    return {
        "scheme": scheme,
        "host": host,
        "port": port,
        "path": path
    }


def main():
    print("=== Configuración de objetivo ===")

    target_input = input("Objetivo (IP, dominio o URL): ").strip()
    lhost = input("Tu IP (LHOST): ").strip()
    lport = input("Puerto de escucha (LPORT): ").strip()

    try:
        lport = int(lport)
    except ValueError:
        print("[!] Puerto inválido")
        return

    parsed = parse_target(target_input)

    print("\n=== Resultado del análisis ===")
    print(f"Protocolo : {parsed['scheme']}")
    print(f"Host      : {parsed['host']}")
    print(f"Puerto    : {parsed['port']}")
    print(f"Path      : {parsed['path']}")

    print("\n=== Configuración sugerida ===")
    print(f"RHOSTS    : {parsed['host']}")
    print(f"RPORT     : {parsed['port']}")
    print(f"TARGETURI : {parsed['path']}")
    print(f"LHOST     : {lhost}")
    print(f"LPORT     : {lport}")

    print("\n[+] Usa estos valores en tu herramienta de pruebas.")


if __name__ == "__main__":
    main()
