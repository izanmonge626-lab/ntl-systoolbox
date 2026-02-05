cat > install.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

echo "==========================================="
echo "   Installation de NTL-SysToolbox (Linux)"
echo "==========================================="

# Toujours se placer dans le dossier du script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "[1/5] Installation des dépendances système (sudo)..."
if command -v apt >/dev/null 2>&1; then
  sudo apt update -y
  sudo apt install -y python3-full python3-venv python3-pip git
else
  echo "[ERREUR] 'apt' non trouvé. Installe python3-venv + python3-pip avec ton gestionnaire de paquets."
  exit 1
fi

echo "[2/5] Création de l'environnement virtuel (user)..."
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

echo "[3/5] Activation du venv..."
# shellcheck disable=SC1091
source venv/bin/activate

echo "[4/5] Installation des dépendances Python..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "[5/5] Configuration..."
# Crée config/config.json si absent
if [ ! -f "config/config.json" ] && [ -f "config/config.example.json" ]; then
  cp -f "config/config.example.json" "config/config.json"
fi

# Compat si le code cherche encore src/config/config.json
mkdir -p "src/config"
if [ -f "config/config.json" ] && [ ! -f "src/config/config.json" ]; then
  cp -f "config/config.json" "src/config/config.json"
fi

echo "✅ Installation terminée !"
echo "-------------------------------------------"
echo "Pour lancer l'outil :"
echo "cd \"$SCRIPT_DIR\""
echo "source venv/bin/activate"
echo "python3 src/main.py"
echo "-------------------------------------------"
EOF

chmod +x install.sh