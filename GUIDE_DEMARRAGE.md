# 🚀 GUIDE DE DÉMARRAGE RAPIDE - NTL-SysToolbox

## 📦 Ce que vous avez

Une **structure de projet complète et fonctionnelle** avec :
- ✅ 3 modules Python opérationnels
- ✅ Menu CLI interactif
- ✅ Configuration exemple
- ✅ Base de données EOL
- ✅ Documentation de base

## 🎯 Prochaines étapes IMMÉDIATEMENT

### 1. Extraire l'archive (2 min)

```bash
# Sur votre PC
cd /chemin/vers/votre/projet
tar -xzf NTL-SysToolbox.tar.gz
cd NTL-SysToolbox
```

### 2. Pousser sur GitLab (5 min)

```bash
# Initialiser Git
git init
git add .
git commit -m "feat: Structure initiale du projet"

# Lier à votre GitLab local
git remote add origin http://votre-gitlab/votre-groupe/ntl-systoolbox.git
git push -u origin main

# Créer branches de travail
git checkout -b dev
git push -u origin dev

git checkout -b feature/diagnostic
git checkout -b feature/backup
git checkout -b feature/audit
```

### 3. Configurer l'outil (10 min)

```bash
# Copier le fichier de config
cp config/config.example.json config/config.json

# Éditer avec vos IPs de VMs
nano config/config.json  # ou votre éditeur préféré
```

**Modifiez ces valeurs :**
```json
{
  "diagnostic": {
    "mysql_servers": [
      {
        "ip": "192.168.X.Y",  ← IP de votre VM Ubuntu
        "username": "votre_user",
        "password": "votre_mdp"
      }
    ],
    "ad_dns_servers": [
      {
        "ip": "192.168.X.Z",  ← IP de votre VM Windows Server
        "username": "Administrator",
        "password": "votre_mdp"
      }
    ]
  },
  "audit": {
    "network_ranges": [
      "192.168.X.0/24"  ← Votre plage réseau
    ]
  }
}
```

### 4. Installer les dépendances (5 min)

```bash
# Optionnel mais recommandé : environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les packages
pip install -r requirements.txt
```

### 5. Premier test (5 min)

```bash
cd src
python main.py
```

Vous devriez voir le menu interactif ! 🎉

## 🧪 Tests à faire MERCREDI

### Test 1 : MySQL (Module Diagnostic)
```bash
python main.py
# Choix 1 : Vérifier MySQL
```
**Attendu :** Connexion réussie, version affichée

### Test 2 : Sauvegarde (Module Backup)
```bash
python main.py
# Choix 5 : Sauvegarde base
```
**Attendu :** Fichier .sql dans outputs/backups/

### Test 3 : Scan réseau (Module Audit)
```bash
python main.py
# Choix 7 : Scanner réseau
# Entrer: 192.168.X.0/24
```
**Attendu :** Détection de vos 3 machines (hôte + 2 VMs)

## 🐛 Dépannage rapide

### Erreur "Module not found"
```bash
# Vérifier que vous êtes dans le bon dossier
pwd  # Doit être dans NTL-SysToolbox/src ou NTL-SysToolbox

# Réinstaller les dépendances
pip install -r requirements.txt
```

### Erreur "Connection refused" MySQL
- Vérifier que MySQL est démarré sur la VM
- Vérifier l'IP dans config.json
- Vérifier le firewall de la VM
- Tester : `ping 192.168.X.Y` depuis le PC hôte

### Erreur "File not found" config
```bash
# Créer le fichier de config
cp config/config.example.json config/config.json
```

## 📝 Répartition suggérée

### Personne 1 - Module Diagnostic
- Tester et améliorer diagnostic.py
- Gérer connexions distantes Windows/Linux
- Documenter le module
- Démo en soutenance

### Personne 2 - Module Backup
- Tester et améliorer backup.py
- Gérer compression
- Tester restauration
- Documenter le module
- Démo en soutenance

### Personne 3 - Module Audit
- Tester et améliorer audit.py
- Optimiser scan réseau
- Enrichir base EOL
- Documenter le module
- Démo en soutenance

### Personne 4 - Intégration & Documentation
- Tests d'intégration
- Documentation générale
- Manuel installation/utilisation
- Dossier technique
- Présentation PowerPoint
- Coordination

## 🎬 Checklist pour la soutenance

### Avant vendredi
- [ ] Code qui fonctionne sur vos VMs
- [ ] Repo Git propre avec historique
- [ ] README complet
- [ ] 3 documents livrables rédigés
- [ ] Rapport EOL généré
- [ ] Présentation PowerPoint prête
- [ ] Démo répétée 3x

### Le jour J
- [ ] VMs démarrées et testées
- [ ] Code à jour sur toutes les machines
- [ ] Fichiers de demo prêts
- [ ] Présentation chargée
- [ ] Équipe coordonnée
- [ ] Être détendu ! 😊

## 💪 Vous êtes prêts !

**Ce que vous avez :**
- Un projet structuré professionnellement
- Du code fonctionnel et propre
- Une base solide pour travailler

**Ce qu'il vous reste à faire :**
- Tester et adapter à votre environnement
- Corriger les petits bugs
- Documenter
- Présenter

**Temps estimé :**
- Mercredi : 6-8h de tests/corrections
- Jeudi : 6-8h de doc/préparation
- Vendredi matin : 2h de derniers ajustements

## 📞 En cas de problème

Si vous êtes bloqués :
1. Consultez README.md et STRUCTURE.md
2. Regardez TODO.md pour les priorités
3. Vérifiez les logs dans outputs/logs/
4. Testez sur machine locale d'abord
5. Puis sur VMs

## 🚀 Allez-y, vous allez cartonner !

N'oubliez pas :
- **Le projet est faisable en 3 jours**
- **Le code de base est là**
- **Vous avez une équipe**
- **Faites-vous confiance !**

Bon courage ! 💪🔥
