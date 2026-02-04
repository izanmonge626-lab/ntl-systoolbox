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
    print("    3. Informations serveur Windows")
    print("    4. Informations serveur Linux")
    print()
    print("  💾 MODULE 2 - SAUVEGARDE WMS")
    print("  ─────────────────────────────")
    print("    5. Sauvegarde complète base de données (SQL)")
    print("    6. Export d'une table en CSV")
    print()
    print("  🔍 MODULE 3 - AUDIT D'OBSOLESCENCE")
    print("  ──────────────────────────────────")
    print("    7. Scanner le réseau")
    print("    8. Générer rapport EOL complet")
    print("    9. Vérifier EOL d'un OS spécifique")
    print()
    print("  ⚙️  AUTRES")
    print("  ───────────")
    print("    10. Afficher la configuration")
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
        if choice == '1':
            # Vérifier MySQL
            print("\n🔍 Vérification de la base de données MySQL...")
            module = DiagnosticModule(config, logger)
            return module.check_mysql()
        
        elif choice == '2':
            # Vérifier AD/DNS
            print("\n🔍 Vérification des services AD/DNS...")
            module = DiagnosticModule(config, logger)
            return module.check_ad_dns()
        
        elif choice == '3':
            # Info serveur Windows
            print("\n📊 Informations serveur Windows")
            ip = input("  IP du serveur: ").strip()
            if ip:
                module = DiagnosticModule(config, logger)
                return module.get_server_info(ip, os_type='windows')
            else:
                print("❌ Adresse IP requise")
                return False
        
        elif choice == '4':
            # Info serveur Linux
            print("\n📊 Informations serveur Linux")
            ip = input("  IP du serveur: ").strip()
            if ip:
                module = DiagnosticModule(config, logger)
                return module.get_server_info(ip, os_type='linux')
            else:
                print("❌ Adresse IP requise")
                return False
        
        elif choice == '5':
            # Sauvegarde SQL
            print("\n💾 Sauvegarde complète de la base de données...")
            module = BackupModule(config, logger)
            return module.backup_database()
        
        elif choice == '6':
            # Export CSV
            print("\n💾 Export d'une table en CSV")
            table = input("  Nom de la table: ").strip()
            if table:
                module = BackupModule(config, logger)
                return module.export_table_csv(table)
            else:
                print("❌ Nom de table requis")
                return False
        
        elif choice == '7':
            # Scanner réseau
            print("\n🔍 Scanner le réseau")
            network = input("  Plage réseau (ex: 192.168.10.0/24): ").strip()
            if network:
                module = AuditModule(config, logger)
                return module.scan_network(network)
            else:
                print("❌ Plage réseau requise")
                return False
        
        elif choice == '8':
            # Rapport EOL complet
            print("\n📋 Génération du rapport d'obsolescence complet...")
            module = AuditModule(config, logger)
            return module.generate_eol_report()
        
        elif choice == '9':
            # Vérifier EOL d'un OS
            print("\n🔍 Vérifier la fin de vie d'un OS")
            print("  OS disponibles: Windows Server, Ubuntu, CentOS, Debian, Windows 10, Windows 11")
            os_name = input("  Nom de l'OS: ").strip()
            version = input("  Version: ").strip()
            if os_name and version:
                module = AuditModule(config, logger)
                return module.check_os_eol(os_name, version)
            else:
                print("❌ OS et version requis")
                return False
        
        elif choice == '10':
            # Afficher config
            print("\n⚙️  Configuration actuelle")
            print("─" * 60)
            print(f"Niveau de log: {config.get('general', {}).get('log_level', 'INFO')}")
            print(f"Répertoire de sortie: {config.get('general', {}).get('output_dir', 'outputs')}")
            print(f"Serveurs MySQL configurés: {len(config.get('diagnostic', {}).get('mysql_servers', []))}")
            print(f"Serveurs AD/DNS configurés: {len(config.get('diagnostic', {}).get('ad_dns_servers', []))}")
            print(f"Plages réseau à auditer: {len(config.get('audit', {}).get('network_ranges', []))}")
            print("─" * 60)
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
