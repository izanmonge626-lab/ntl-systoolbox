# NTL-SysToolbox

Outil en ligne de commande pour l'administration système de NordTransit Logistics.

## Description

NTL-SysToolbox est un utilitaire CLI qui industrialise les vérifications d'exploitation, sécurise la gestion des sauvegardes de la base métier et produit un audit d'obsolescence pour l'infrastructure IT de NTL.

## Modules

1. **Module Diagnostic** : Vérification des services critiques (AD/DNS, MySQL, état serveurs)
2. **Module Sauvegarde WMS** : Export et sauvegarde de la base de données MySQL
3. **Module Audit d'obsolescence** : Scan réseau et détection des systèmes en fin de vie

## Prérequis

- Python 3.8 ou supérieur
- Accès réseau aux serveurs à auditer
- Droits d'administration selon les opérations

### Bibliothèques Python requises

```bash
pip install -r requirements.txt
```

## Installation

1. Cloner le dépôt :
```bash
git clone <url-du-depot>
cd NTL-SysToolbox
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurer l'outil :
```bash
cp config/config.example.json config/config.json
# Éditer config/config.json avec vos paramètres
```

## Utilisation

### Lancement du menu interactif

```bash
python src/main.py
```

### Utilisation en ligne de commande directe

```bash
# Module Diagnostic
python src/main.py --module diagnostic --check mysql
python src/main.py --module diagnostic --check ad-dns
python src/main.py --module diagnostic --server-info <ip>

# Module Sauvegarde
python src/main.py --module backup --type sql
python src/main.py --module backup --type csv --table <nom_table>

# Module Audit
python src/main.py --module audit --scan-network <plage_ip>
python src/main.py --module audit --eol-report
```

## Configuration

Le fichier `config/config.json` contient tous les paramètres nécessaires :

- Informations de connexion aux serveurs
- Plages réseau à scanner
- Chemins de sauvegarde
- Seuils d'alerte

**Important** : Ne jamais commiter le fichier `config.json` avec des credentials réels.

## Sorties

Toutes les sorties sont disponibles dans le dossier `outputs/` :

- **logs/** : Logs d'exécution horodatés
- **backups/** : Sauvegardes de la base de données
- **reports/** : Rapports d'audit en JSON et CSV

## Structure du projet

```
NTL-SysToolbox/
├── src/
│   ├── main.py              # Point d'entrée principal
│   ├── cli_menu.py          # Interface CLI interactive
│   ├── modules/
│   │   ├── diagnostic.py    # Module diagnostic
│   │   ├── backup.py        # Module sauvegarde
│   │   └── audit.py         # Module audit obsolescence
│   └── utils/
│       ├── config_loader.py # Chargement configuration
│       ├── logger.py        # Gestion des logs
│       └── network.py       # Utilitaires réseau
├── config/
│   ├── config.example.json  # Exemple de configuration
│   └── eol_database.json    # Base de données EOL
├── docs/
│   ├── installation.md      # Guide d'installation
│   ├── utilisation.md       # Manuel d'utilisation
│   └── technique.md         # Documentation technique
├── tests/                   # Tests unitaires
├── outputs/                 # Sorties générées
├── requirements.txt         # Dépendances Python
└── README.md               # Ce fichier
```

## Codes de retour

- **0** : Succès
- **1** : Erreur générale
- **2** : Erreur de configuration
- **3** : Erreur de connexion
- **4** : Erreur d'authentification
- **5** : Erreur de données

## Équipe projet

- Membre 1 : Module Diagnostic
- Membre 2 : Module Sauvegarde
- Membre 3 : Module Audit
- Membre 4 : Documentation & Intégration

## Licence

Projet académique - MSPR TPRE511 - 2025-2026
