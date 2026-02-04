#!/bin/bash
# Script de démarrage rapide pour NTL-SysToolbox

echo "=========================================="
echo "  NTL-SysToolbox - Installation rapide"
echo "=========================================="
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

echo "✅ Python 3 détecté: $(python3 --version)"
echo ""

# Créer un environnement virtuel (optionnel mais recommandé)
read -p "Créer un environnement virtuel ? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
    
    echo "🔧 Activation de l'environnement..."
    source venv/bin/activate
fi

# Installer les dépendances
echo ""
echo "📦 Installation des dépendances..."
pip install -r requirements.txt

# Copier le fichier de configuration
if [ ! -f "config/config.json" ]; then
    echo ""
    echo "📝 Création du fichier de configuration..."
    cp config/config.example.json config/config.json
    echo "⚠️  N'oubliez pas d'éditer config/config.json avec vos paramètres !"
fi

echo ""
echo "=========================================="
echo "  ✅ Installation terminée !"
echo "=========================================="
echo ""
echo "Pour lancer l'outil:"
echo "  cd src"
echo "  python main.py"
echo ""
echo "Ou en mode commande directe:"
echo "  python src/main.py --module diagnostic --action check-mysql"
echo ""
