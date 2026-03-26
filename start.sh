#!/usr/bin/env bash
# WodZone — arranca todo con un solo comando
# Uso: ./start.sh

set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"

# ── colores ──────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
info()    { echo -e "${GREEN}[WodZone]${NC} $*"; }
warn()    { echo -e "${YELLOW}[WodZone]${NC} $*"; }
error()   { echo -e "${RED}[WodZone]${NC} $*"; }

# ── limpieza al salir ─────────────────────────────────────
cleanup() {
    echo ""
    warn "Deteniendo servicios..."
    [ -n "$PID_DJANGO"   ] && kill "$PID_DJANGO"   2>/dev/null
    [ -n "$PID_FRONTEND" ] && kill "$PID_FRONTEND" 2>/dev/null
    info "Hasta luego."
}
trap cleanup EXIT INT TERM

# ── 1. Django ─────────────────────────────────────────────
info "Iniciando Django en http://127.0.0.1:8000 ..."
cd "$ROOT"
python3 manage.py runserver --noreload > /tmp/wodzone-django.log 2>&1 &
PID_DJANGO=$!

# ── 2. Frontend Vite ──────────────────────────────────────
info "Iniciando frontend en http://localhost:5173 ..."
cd "$ROOT/frontend"
npm run dev > /tmp/wodzone-frontend.log 2>&1 &
PID_FRONTEND=$!
cd "$ROOT"

# ── 3. Esperar a que los servidores respondan ─────────────
wait_for() {
    local url="$1" label="$2" attempts=0
    printf "${GREEN}[WodZone]${NC} Esperando %-20s" "$label ..."
    until curl -s "$url" > /dev/null 2>&1; do
        sleep 1
        attempts=$((attempts + 1))
        if [ $attempts -ge 30 ]; then
            echo ""
            error "Timeout esperando $label. Revisa /tmp/wodzone-${label,,}.log"
            exit 1
        fi
        printf "."
    done
    echo " listo"
}

wait_for "http://127.0.0.1:8000/"              "Django"
wait_for "http://localhost:5173"               "Frontend"

# ── 4. Scanner ────────────────────────────────────────────
echo ""
info "==========================================="
info "  Todo listo. Lanzando escáner QR..."
info "==========================================="
echo ""
python3 "$ROOT/scanner_client.py"
