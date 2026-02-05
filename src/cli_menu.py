#!/usr/bin/env python3
"""
Module de gestion du menu CLI interactif
"""

from modules.diagnostic import DiagnosticModule
from modules.backup import BackupModule
from modules.audit import AuditModule


def display_menu():
    """Affiche le menu principal"""
    print("\n" + "=" * 60)
    print("  MENU PRINCIPAL - NTL-SysToolbox")
    print("=" * 60)
    print()
    print("  📊 MODULE 1 - DIAGNOSTIC")
    print("  ─────────────────────────")
    print("    1. Vérifier la base de données MySQL")
    print("    2. Vérifier les services AD/DNS")
    print("    3. État synthétique machine hôte")
    print()
    print("  💾 MODULE 2 - SAUVEGARDE WMS")
    print("  ─────────────────────────────")
    print("    4. Sauvegarde complète base de données (SQL)")
    print("    5. Export d'une table en CSV")
    print()
    print("  🔍 MODULE 3 - AUDIT D'OBSOLESCENCE")
    print("  ──────────────────────────────────")
    print("    6. Scanner le réseau")
    print("    7. Générer rapport EOL complet")
    print("    8. Vérifier EOL d'un OS spécifique")
    print()
    print("  ⚙️  AUTRES")
    print("  ───────────")
    print("    9. Afficher la configuration")
    print("    0. Quitter")
    print()
    print("=" * 60)


def handle_menu_choice(choice, config, logger):
    """
    Traite le choix de l'utilisateur

    Args:
        choice: Le choix de l'utilisateur (str)
        config: Configuration chargée
        logger: Logger configuré

    Returns:
        bool: True si l'opération a réussi
    """
    try:
        # Module 1
        if choice == "1":
            print("\n🔍 Vérification de la base de données MySQL...")
            module = DiagnosticModule(config, logger)
            return module.check_mysql()

        elif choice == "2":
            print("\n🔍 Vérification des services AD/DNS...")
            module = DiagnosticModule(config, logger)
            return module.check_ad_dns()

        elif choice == "3":
            print("\n📊 État synthétique machine hôte")
            module = DiagnosticModule(config, logger)
            return module.host_synthetic_state()

        # Module 2
        elif choice == "4":
            print("\n💾 Sauvegarde complète de la base de données...")
            module = BackupModule(config, logger)
            return module.backup_database()

        elif choice == "5":
            print("\n💾 Export d'une table en CSV")
            table = input("  Nom de la table: ").strip()
            if not table:
                print("❌ Nom de table requis")
                return False
            module = BackupModule(config, logger)
            return module.export_table_csv(table)

        # Module 3
        elif choice == "6":
            print("\n🔍 Scanner le réseau")
            network = input("  Plage réseau (ex: 192.168.10.0/24): ").strip()
            if not network:
                print("❌ Plage réseau requise")
                return False
            module = AuditModule(config, logger)
            return module.scan_network(network)

        elif choice == "7":
            print("\n📋 Génération du rapport d'obsolescence complet...")
            module = AuditModule(config, logger)
            return module.generate_eol_report()

        elif choice == "8":
            print("\n🔍 Vérifier la fin de vie d'un OS")
            os_name = input("  Nom de l'OS: ").strip()
            version = input("  Version: ").strip()
            if not os_name or not version:
                print("❌ OS et version requis")
                return False
            module = AuditModule(config, logger)
            return module.check_os_eol(os_name, version)

        # Autres
        elif choice == "9":
            print("\n⚙️  Configuration actuelle")
            print("─" * 60)
            print(f"Niveau de log: {config.get('general', {}).get('log_level', 'INFO')}")
            print(f"Répertoire de sortie: {config.get('general', {}).get('output_dir', 'outputs')}")
            print(f"Serveurs MySQL configurés: {len(config.get('diagnostic', {}).get('mysql_servers', []))}")
            print(f"Serveurs AD/DNS configurés: {len(config.get('diagnostic', {}).get('ad_dns_servers', []))}")
            print(f"Plages réseau à auditer: {len(config.get('audit', {}).get('network_ranges', []))}")
            print("─" * 60)
            return True

        elif choice == "0":
            return True

        else:
            print(f"\n❌ Choix invalide: {choice}")
            return False

    except KeyboardInterrupt:
        print("\n\n⚠️  Opération annulée par l'utilisateur")
        return False

    except Exception as e:
        logger.error(f"Erreur lors du traitement du choix {choice}: {e}")
        print(f"\n❌ Erreur: {e}")
        return False