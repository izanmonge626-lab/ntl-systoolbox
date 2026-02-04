# Structure du projet NTL-SysToolbox

## Vue d'ensemble de l'arborescence

```
NTL-SysToolbox/
│
├── README.md                    # Documentation principale
├── requirements.txt             # Dépendances Python
├── .gitignore                   # Fichiers à ignorer par Git
├── quick_start.sh              # Script d'installation rapide
│
├── config/                      # Configuration
│   ├── config.example.json     # Exemple de configuration
│   ├── config.json             # Configuration réelle (à créer)
│   └── eol_database.json       # Base de données End-of-Life
│
├── src/                         # Code source
│   ├── __init__.py
│   ├── main.py                 # Point d'entrée principal
│   ├── cli_menu.py             # Menu CLI interactif
│   │
│   ├── modules/                # Modules fonctionnels
│   │   ├── __init__.py
│   │   ├── diagnostic.py      # Module 1: Diagnostic
│   │   ├── backup.py          # Module 2: Sauvegarde
│   │   └── audit.py           # Module 3: Audit obsolescence
│   │
│   └── utils/                  # Utilitaires
│       ├── __init__.py
│       ├── config_loader.py   # Chargement config
│       ├── logger.py          # Gestion logs
│       └── network.py         # Utilitaires réseau
│
├── outputs/                    # Fichiers générés
│   ├── logs/                  # Logs d'exécution
│   ├── backups/               # Sauvegardes BDD
│   └── reports/               # Rapports d'audit
│
├── docs/                       # Documentation
│   ├── installation.md        # Guide d'installation
│   ├── utilisation.md         # Manuel d'utilisation
│   └── technique.md           # Documentation technique
│
├── tests/                      # Tests unitaires
│
└── data/                       # Données temporaires
```

## Description des composants

### 📂 Dossiers principaux

#### `config/`
Contient tous les fichiers de configuration :
- **config.example.json** : Template de configuration (versionné)
- **config.json** : Configuration réelle avec credentials (NON versionné)
- **eol_database.json** : Base de données des dates de fin de vie des OS

#### `src/`
Code source de l'application :
- **main.py** : Point d'entrée, gestion des arguments CLI
- **cli_menu.py** : Interface menu interactif
- **modules/** : Les 3 modules fonctionnels (diagnostic, backup, audit)
- **utils/** : Fonctions utilitaires partagées

#### `outputs/`
Sorties générées par l'outil :
- **logs/** : Logs d'exécution horodatés
- **backups/** : Fichiers de sauvegarde MySQL (.sql, .csv)
- **reports/** : Rapports d'audit (JSON, CSV)

⚠️ Ce dossier est ignoré par Git (sauf les .gitkeep)

#### `docs/`
Documentation du projet :
- Guide d'installation
- Manuel d'utilisation
- Documentation technique

#### `tests/`
Tests unitaires et d'intégration (à développer)

### 📄 Fichiers clés

#### `main.py`
Point d'entrée principal qui :
- Parse les arguments de ligne de commande
- Configure le logger
- Charge la configuration
- Lance le mode interactif OU exécute une commande

#### `cli_menu.py`
Gère l'interface menu interactif :
- Affiche le menu
- Traite les choix utilisateur
- Appelle les modules appropriés

#### Modules fonctionnels

**diagnostic.py** - Module 1
- `check_mysql()` : Vérifie les serveurs MySQL
- `check_ad_dns()` : Vérifie les services AD/DNS
- `get_server_info()` : Collecte infos serveur (CPU, RAM, disque)

**backup.py** - Module 2
- `backup_database()` : Sauvegarde complète MySQL
- `export_table_csv()` : Export d'une table en CSV
- Support mysqldump + méthode Python alternative

**audit.py** - Module 3
- `scan_network()` : Scan d'une plage réseau
- `generate_eol_report()` : Rapport d'obsolescence complet
- `check_os_eol()` : Vérifie EOL d'un OS spécifique

#### Utilitaires

**config_loader.py**
- Chargement et validation de la configuration
- Support variables d'environnement
- Gestion des chemins

**logger.py**
- Configuration du système de logging
- Logs console + fichier
- Niveaux configurables

**network.py**
- Validation IP/réseau
- Ping d'hôtes
- Résolution DNS
- Test de ports

## Flux d'exécution

### Mode interactif
```
main.py → cli_menu.py → display_menu()
                      → handle_menu_choice()
                      → module.fonction()
                      → résultat + sauvegarde
```

### Mode ligne de commande
```
main.py --module X --action Y → parse_arguments()
                              → run_command_mode()
                              → module.fonction()
                              → exit code
```

## Formats de sortie

### Logs
```
2025-02-03 14:30:15 - NTL-SysToolbox - INFO - Message
```

### Rapports JSON
```json
{
  "check_type": "mysql_check",
  "timestamp": "2025-02-03T14:30:15",
  "results": [...]
}
```

### Exports CSV
```
ip;hostname;os;version;eol_status;eol_date
192.168.10.10;DC01;Windows Server;2019;ACTIVE;2029-01-09
```

## Configuration Git

### Branches recommandées
- `main` : Branche principale
- `dev` : Développement
- `feature/diagnostic` : Module diagnostic
- `feature/backup` : Module backup
- `feature/audit` : Module audit

### Commits types
- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Documentation
- `refactor:` Refactorisation
- `test:` Tests

## Points d'attention

⚠️ **Sécurité**
- Ne jamais commiter `config/config.json`
- Utiliser des variables d'environnement pour les secrets
- Logs : attention aux mots de passe

⚠️ **Performance**
- Scan réseau : peut être long sur grandes plages
- Sauvegarde MySQL : dépend de la taille de la BDD
- Timeout configurables

⚠️ **Dépendances**
- `mysql-connector-python` : Requis pour MySQL
- `python-nmap` : Optionnel (scan avancé)
- `paramiko` : Optionnel (SSH)
- `pywinrm` : Optionnel (WinRM)

## Prochaines étapes

Pour compléter le projet :

1. ✅ Structure de base créée
2. ✅ Modules fonctionnels implémentés
3. 🔲 Tests sur VMs
4. 🔲 Documentation détaillée
5. 🔲 Gestion d'erreurs avancée
6. 🔲 Tests unitaires
7. 🔲 Préparation soutenance
