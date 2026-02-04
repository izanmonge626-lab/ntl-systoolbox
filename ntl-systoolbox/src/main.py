#!/usr/bin/env python3
"""
NTL-SysToolbox - Outil d'administration système pour NordTransit Logistics
Point d'entrée principal de l'application
"""

import sys
import argparse
from pathlib import Path

# Ajout du dossier src au PATH pour les imports
sys.path.insert(0, str(Path(__file__).parent))

from cli_menu import display_menu, handle_menu_choice
from utils.logger import setup_logger
from utils.config_loader import load_config

__version__ = "1.0.0"


def parse_arguments():
    """Parse les arguments de ligne de commande"""
    parser = argparse.ArgumentParser(
        description="NTL-SysToolbox - Outil d'administration système",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  # Mode interactif (recommandé)
  python main.py
  
  # Module Diagnostic
  python main.py --module diagnostic --action check-mysql
  python main.py --module diagnostic --action check-ad-dns
  python main.py --module diagnostic --action server-info --target 192.168.10.21
  
  # Module Sauvegarde
  python main.py --module backup --action sql-dump
  python main.py --module backup --action csv-export --table orders
  
  # Module Audit
  python main.py --module audit --action scan-network --network 192.168.10.0/24
  python main.py --module audit --action eol-report
        """
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'NTL-SysToolbox v{__version__}'
    )
    
    parser.add_argument(
        '--module',
        choices=['diagnostic', 'backup', 'audit'],
        help='Module à exécuter'
    )
    
    parser.add_argument(
        '--action',
        help='Action à effectuer dans le module'
    )
    
    parser.add_argument(
        '--target',
        help='Cible de l\'action (IP, hostname, etc.)'
    )
    
    parser.add_argument(
        '--table',
        help='Nom de la table pour export CSV'
    )
    
    parser.add_argument(
        '--network',
        help='Plage réseau à scanner (format CIDR)'
    )
    
    parser.add_argument(
        '--config',
        default='config/config.json',
        help='Chemin vers le fichier de configuration (défaut: config/config.json)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Active le mode debug'
    )
    
    return parser.parse_args()


def run_cli_mode(config, logger):
    """Execute le mode CLI interactif"""
    logger.info("Démarrage du mode interactif")
    
    while True:
        try:
            display_menu()
            choice = input("\n➤ Votre choix : ").strip()
            
            if choice == '0':
                logger.info("Arrêt de l'application")
                print("\n👋 Au revoir !")
                break
            
            result = handle_menu_choice(choice, config, logger)
            
            if result:
                input("\n⏎ Appuyez sur Entrée pour continuer...")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Interruption par l'utilisateur")
            logger.warning("Interruption par l'utilisateur (Ctrl+C)")
            break
        except Exception as e:
            logger.error(f"Erreur dans le menu: {e}")
            print(f"\n❌ Erreur: {e}")
            input("\n⏎ Appuyez sur Entrée pour continuer...")


def run_command_mode(args, config, logger):
    """Execute une commande directe (mode non-interactif)"""
    logger.info(f"Exécution du module {args.module} avec action {args.action}")
    
    if args.module == 'diagnostic':
        from modules.diagnostic import DiagnosticModule
        module = DiagnosticModule(config, logger)
        
        if args.action == 'check-mysql':
            return module.check_mysql()
        elif args.action == 'check-ad-dns':
            return module.check_ad_dns()
        elif args.action == 'server-info' and args.target:
            return module.get_server_info(args.target)
        else:
            print("❌ Action invalide pour le module diagnostic")
            return False
    
    elif args.module == 'backup':
        from modules.backup import BackupModule
        module = BackupModule(config, logger)
        
        if args.action == 'sql-dump':
            return module.backup_database()
        elif args.action == 'csv-export' and args.table:
            return module.export_table_csv(args.table)
        else:
            print("❌ Action invalide pour le module backup")
            return False
    
    elif args.module == 'audit':
        from modules.audit import AuditModule
        module = AuditModule(config, logger)
        
        if args.action == 'scan-network' and args.network:
            return module.scan_network(args.network)
        elif args.action == 'eol-report':
            return module.generate_eol_report()
        else:
            print("❌ Action invalide pour le module audit")
            return False
    
    return False


def main():
    """Fonction principale"""
    print("=" * 60)
    print("  NTL-SysToolbox - Administration Système NTL")
    print(f"  Version {__version__}")
    print("=" * 60)
    print()
    
    # Parse des arguments
    args = parse_arguments()
    
    # Configuration du logger
    log_level = 'DEBUG' if args.debug else 'INFO'
    logger = setup_logger(level=log_level)
    
    try:
        # Chargement de la configuration
        logger.info(f"Chargement de la configuration depuis {args.config}")
        config = load_config(args.config)
        
        # Mode d'exécution
        if args.module:
            # Mode commande directe
            success = run_command_mode(args, config, logger)
            sys.exit(0 if success else 1)
        else:
            # Mode interactif
            run_cli_mode(config, logger)
            sys.exit(0)
    
    except FileNotFoundError as e:
        logger.error(f"Fichier non trouvé: {e}")
        print(f"❌ Fichier non trouvé: {e}")
        print(f"💡 Vérifiez que le fichier de configuration existe: {args.config}")
        sys.exit(2)
    
    except Exception as e:
        logger.error(f"Erreur fatale: {e}", exc_info=True)
        print(f"❌ Erreur fatale: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
