#!/usr/bin/env bash
# ==============================================================================
# Protocolo C5-REAL: Verificación de Contraseñas por k-Anonimato
# Exergía: Máxima. No transmite la contraseña ni el hash completo a la red.
# ==============================================================================

set -euo pipefail

if [ $# -eq 0 ]; then
    echo "[-] Error: Especifica la contraseña o hash a auditar."
    echo "    Uso: $0 \"TuContraseñaAComprobar\""
    exit 1
fi

PASSWORD="$1"

# 1. Obtener el hash SHA-1 en mayúsculas sin salto de línea
if command -v shasum >/dev/null 2>&1; then
    SHA1_HASH=$(echo -n "$PASSWORD" | shasum -a 1 | awk '{print toupper($1)}')
elif command -v openssl >/dev/null 2>&1; then
    SHA1_HASH=$(echo -n "$PASSWORD" | openssl sha1 | awk '{print toupper($2)}')
else
    echo "[-] Error: Se requiere 'openssl' o 'shasum' en el entorno local."
    exit 1
fi

# 2. Extraer prefijo (primeros 5 caracteres) y sufijo (resto)
PREFIX="${SHA1_HASH:0:5}"
SUFFIX="${SHA1_HASH:5}"

echo "[+] Auditando prefijo de k-Anonimato: $PREFIX..."

# 3. Consultar la API de Pwned Passwords enviando SOLO los 5 caracteres del prefijo
RESPONSE=$(curl -s --fail "https://api.pwnedpasswords.com/range/$PREFIX" || true)

if [ -z "$RESPONSE" ]; then
    echo "[-] Error: No se pudo conectar a la API de Pwned Passwords."
    exit 1
fi

# 4. Buscar coincidencia exacta del sufijo en las respuestas
MATCH=$(echo "$RESPONSE" | grep -i "^$SUFFIX" || true)

if [ -n "$MATCH" ]; then
    COUNT=$(echo "$MATCH" | cut -d':' -f2 | tr -d '\r')
    echo -e "\033[0;31m[!] ALERTA CRÍTICA: Esta contraseña ha aparecido $COUNT veces en filtraciones de datos.\033[0m"
    echo "[!] Invariante rota: Se requiere rotación inmediata y migración a FIDO2/Passkey."
    exit 2
else
    echo -e "\033[0;32m[✓] OK: Cero coincidencias registradas para la firma en la base de datos de filtraciones.\033[0m"
    exit 0
fi
