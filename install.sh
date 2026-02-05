#!/bin/bash

echo "==========================================="
echo "   Installation de NTL-SysToolbox (Linux)"
echo "==========================================="

# Vérification des droits sudo
if [ "$EUID" -ne 0 ]; then
    echo "Veuillez exécuter ce script avec sudo."
    exit 1
fi

echo "[1/5] Mise à jour des paquets..."
apt update -y

echo "[2/5] Installation des dépendances système..."
apt install -y python3-full python3-venv python3-pip git



cd ntl-systoolbox

echo "[3/5] Création de l'environnement virtuel..."
python3 -m venv venv

echo "[4/5] Activation du venv et installation des dépendances Linux..."
source venv/bin/activate

# Dépendances Linux uniquement
pip install \
    paramiko \
    mysql-connector-python \
    pymysql \
    python-nmap \
    scapy \
    psutil \
    click \
    colorama \
    rich \
    tabulate \
    PyYAML \
    python-dotenv \
    requests \
    validators \
    python-dateutil \
    py-cpuinfo \
    distro \
    flask

echo "[5/5] Installation terminée !"
echo "-------------------------------------------"
echo "Pour lancer l'outil :"
echo "cd ntl-systoolbox"
echo "source venv/bin/activate"
echo "python3 src/main.py"
echo "-------------------------------------------"