# TODO - NTL-SysToolbox

## ✅ FAIT (Mardi soir)

- [x] Structure complète du projet créée
- [x] Configuration de base (config.json, eol_database.json)
- [x] Module Diagnostic fonctionnel (MySQL, AD/DNS, infos serveur)
- [x] Module Backup fonctionnel (dump SQL, export CSV)
- [x] Module Audit fonctionnel (scan réseau, rapport EOL)
- [x] Menu CLI interactif
- [x] Système de logging
- [x] Utilitaires réseau
- [x] Documentation README et STRUCTURE

## 🔥 PRIORITÉS MERCREDI (jour 1)

### Matin (4h)
1. **Setup Git** (30 min)
   - Initialiser repo sur GitLab local
   - Premier commit avec structure
   - Créer branches dev + feature/xxx

2. **Configuration** (1h)
   - Copier config.example.json → config.json
   - Remplir avec IPs de vos VMs
   - Tester connexions

3. **Tests Module Diagnostic** (2h)
   - Test connexion MySQL sur VM Ubuntu
   - Test vérification services sur VM Windows Server
   - Test infos serveur local
   - Corriger bugs éventuels

### Après-midi (4h)
4. **Tests Module Backup** (2h)
   - Créer base de test sur MySQL
   - Tester backup complet
   - Tester export CSV
   - Vérifier fichiers générés

5. **Tests Module Audit** (2h)
   - Scanner plage réseau de vos VMs
   - Vérifier détection des 3 machines
   - Générer rapport EOL complet
   - Valider format CSV/JSON

### Soir (optionnel)
6. **Améliorations rapides** (2h)
   - Gestion d'erreurs
   - Messages utilisateur plus clairs
   - Validation des inputs
   - Commits réguliers sur Git

## 📋 JEUDI (jour 2)

### Matin (4h)
1. **Finalisation code** (2h)
   - Derniers bugs
   - Tests d'intégration
   - Merge sur main

2. **Documentation technique** (2h)
   - Choix techniques justifiés
   - Architecture logique
   - Compromis assumés

### Après-midi (4h)
3. **Manuel installation** (1h)
   - Guide pas-à-pas
   - Prérequis
   - Troubleshooting

4. **Manuel utilisation** (1h)
   - Exemples d'utilisation
   - Captures d'écran
   - Interprétation des sorties

5. **Support présentation** (2h)
   - PowerPoint (10-15 slides)
   - Démo préparée
   - Répartition du speech

### Soir
6. **Répétition** (1h)
   - Chronométrer (20 min max)
   - Répartir qui dit quoi
   - Préparer réponses questions

## 🎯 VENDREDI MATIN (jour 3)

1. **Derniers ajustements** (1h)
   - Vérif que tout fonctionne
   - Repo Git propre
   - Tous les livrables présents

2. **Préparation démo** (1h)
   - Lancer les VMs
   - Tester la démo une dernière fois
   - Backup de secours

3. **Passage** 
   - Respirer 😊
   - Vous allez cartonner ! 🚀

## 📦 LIVRABLES À PRÉPARER

### 1. Code source
- [ ] Repo GitLab avec historique propre
- [ ] README complet
- [ ] Code commenté

### 2. Dossier technique
- [ ] Justification des choix (Python, bibliothèques)
- [ ] Architecture (diagramme ?)
- [ ] Gestion des secrets
- [ ] Compromis assumés

### 3. Manuel installation
- [ ] Prérequis (Python, pip)
- [ ] Installation dépendances
- [ ] Configuration
- [ ] Vérification

### 4. Manuel utilisation
- [ ] Lancement de l'outil
- [ ] Exemples pour chaque module
- [ ] Interprétation des sorties
- [ ] Troubleshooting

### 5. Rapport EOL de référence
- [ ] Exécuter audit complet sur vos VMs
- [ ] Fichier JSON + CSV
- [ ] À joindre aux livrables

### 6. Support présentation
- [ ] PowerPoint (~12 slides)
- [ ] Démo préparée
- [ ] Répartition équipe

## 🎬 PLAN DE LA SOUTENANCE (20 min)

### Introduction (2 min)
- Présentation équipe
- Contexte NTL
- Objectifs du projet

### Démarche (3 min)
- Architecture choisie
- Technologies (Python, pourquoi)
- Organisation du travail

### Démonstration (10 min)
- **Module 1** : Vérif MySQL + infos serveur (3 min)
- **Module 2** : Backup + export CSV (3 min)
- **Module 3** : Scan réseau + rapport EOL (4 min)

### Difficultés & Solutions (3 min)
- Challenges rencontrés
- Solutions mises en place
- Apprentissages

### Conclusion (2 min)
- Résultats obtenus
- Améliorations possibles
- Perspectives

## ⚠️ POINTS D'ATTENTION

### Démo live
- Tester 3x avant le passage
- Avoir un plan B (vidéo)
- Prévoir les questions

### Git
- Commits réguliers et clairs
- Messages en français
- Branches propres

### Documentation
- Pas trop longue (max 3-4 pages par doc)
- Concrète et pratique
- Avec exemples

### Répartition équipe
- Personne 1 : Module Diagnostic + démo
- Personne 2 : Module Backup + démo
- Personne 3 : Module Audit + démo
- Personne 4 : Documentation + intégration + présentation intro/conclusion

## 💡 ASTUCES

### Pour gagner du temps
- Ne pas chercher la perfection
- Focus sur le fonctionnel
- Documenter au fur et à mesure

### Pour la démo
- Préparer les commandes à l'avance
- Avoir des données de test
- Chronométrer

### Pour la soutenance
- Être honnête sur les limites
- Montrer ce qui marche
- Expliquer les choix

## 🚀 VOUS AVEZ TOUT CE QU'IL FAUT !

Le code de base est là, fonctionnel et propre.
Maintenant il faut :
1. Tester sur vos VMs
2. Adapter/corriger
3. Documenter
4. Présenter

**Vous allez y arriver ! 💪**
