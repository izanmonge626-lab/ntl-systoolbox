#!/usr/bin/env python3
"""
Module 3 - Audit d'obsolescence
Scan réseau et détection des systèmes en fin de vie
"""

import json
import csv
from datetime import datetime, timedelta
from pathlib import Path
import socket
import platform
import subprocess

try:
    import nmap
    NMAP_AVAILABLE = True
except ImportError:
    NMAP_AVAILABLE = False


class AuditModule:
    """Module d'audit d'obsolescence"""
    
    def __init__(self, config, logger):
        """
        Initialise le module d'audit
        
        Args:
            config: Configuration chargée
            logger: Logger configuré
        """
        self.config = config
        self.logger = logger
        self.audit_config = config.get('audit', {})
        self.output_dir = Path(config['general']['output_dir']) / 'reports'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Charger la base EOL
        self.eol_database = self._load_eol_database()
    
    def _load_eol_database(self):
        """Charge la base de données des dates de fin de vie"""
        eol_file = self.audit_config.get('eol_database_file', 'config/eol_database.json')
        
        # Chemin relatif depuis src/
        if not Path(eol_file).is_absolute():
            eol_file = Path(__file__).parent.parent.parent / eol_file
        
        try:
            with open(eol_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.logger.info(f"Base EOL chargée: {eol_file}")
                return data.get('operating_systems', {})
        except Exception as e:
            self.logger.error(f"Erreur chargement base EOL: {e}")
            return {}
    
    def scan_network(self, network_range):
        """
        Scan d'une plage réseau pour détecter les hôtes actifs
        
        Args:
            network_range: Plage réseau CIDR (ex: 192.168.1.0/24)
        
        Returns:
            bool: True si succès
        """
        self.logger.info(f"=== Début scan réseau {network_range} ===")
        print(f"\n🔍 Scan du réseau {network_range}")
        print("─" * 60)
        
        from utils.network import is_valid_network
        
        if not is_valid_network(network_range):
            print(f"❌ Plage réseau invalide: {network_range}")
            return False
        
        hosts_found = []
        
        if NMAP_AVAILABLE:
            hosts_found = self._scan_with_nmap(network_range)
        else:
            print("⚠️  Nmap non disponible, utilisation méthode basique...")
            hosts_found = self._scan_basic(network_range)
        
        # Sauvegarde des résultats
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # JSON
        json_file = self.output_dir / f"scan_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'scan_date': datetime.now().isoformat(),
                'network': network_range,
                'hosts_found': len(hosts_found),
                'hosts': hosts_found
            }, f, indent=2, ensure_ascii=False)
        
        # CSV
        csv_file = self.output_dir / f"scan_{timestamp}.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['ip', 'hostname', 'os', 'version', 'accuracy', 'status'], delimiter=';')
            for host in hosts_found:
                host.setdefault('accuracy', 0)
            writer.writeheader()
            writer.writerows(hosts_found)
        
        print(f"\n📊 Résultats:")
        print(f"  • Hôtes trouvés: {len(hosts_found)}")
        print(f"  • JSON: {json_file.name}")
        print(f"  • CSV: {csv_file.name}")
        
        self.logger.info(f"Scan terminé: {len(hosts_found)} hôtes trouvés")
        
        return True
    
    def _scan_with_nmap(self, network_range):
        """Scan avec Nmap (détection OS)"""
        print("  🔄 Scan avec Nmap (détection OS activée)...")
        
        hosts = []
        
        try:
            nm = nmap.PortScanner()
            
            # Scan avec détection OS (nécessite droits admin)
            print("  ⏳ Scan en cours (peut prendre plusieurs minutes)...")
            nm.scan(hosts=network_range, arguments='-O -sV --osscan-guess')
            
            for host in nm.all_hosts():
                host_info = {
                    'ip': host,
                    'hostname': nm[host].hostname() if nm[host].hostname() else 'Unknown',
                    'status': nm[host].state(),
                    'os': 'Unknown',
                    'version': 'Unknown'
                }
                
                # Tentative détection OS
                if 'osmatch' in nm[host] and nm[host]['osmatch']:
                    os_match = nm[host]['osmatch'][0]
                    host_info['os'] = os_match.get('name', 'Unknown')
                    host_info['accuracy'] = os_match.get('accuracy', 0)
                
                hosts.append(host_info)
                print(f"    ✓ {host} - {host_info['hostname']} ({host_info['os']})")
        
        except Exception as e:
            print(f"  ⚠️  Erreur Nmap: {e}")
            self.logger.error(f"Erreur scan Nmap: {e}")
        
        return hosts
    
    def _scan_basic(self, network_range):
        """Scan basique avec ping"""
        print("  🔄 Scan basique avec ping...")
        
        from utils.network import get_network_hosts, ping_host
        
        hosts = []
        ips = get_network_hosts(network_range)
        
        print(f"  📡 {len(ips)} adresses à scanner...")
        
        for i, ip in enumerate(ips):
            if (i + 1) % 10 == 0:
                print(f"    Progression: {i+1}/{len(ips)}")
            
            if ping_host(ip, timeout=1):
                try:
                    hostname = socket.gethostbyaddr(ip)[0]
                except:
                    hostname = 'Unknown'
                
                host_info = {
                    'ip': ip,
                    'hostname': hostname,
                    'status': 'up',
                    'os': 'Unknown',
                    'version': 'Unknown'
                }
                
                hosts.append(host_info)
                print(f"    ✓ {ip} - {hostname}")
        
        return hosts
    
    def generate_eol_report(self):
        """
        Génère un rapport d'obsolescence complet
        
        Returns:
            bool: True si succès
        """
        self.logger.info("=== Génération rapport EOL ===")
        print("\n📋 Génération du rapport d'obsolescence")
        print("─" * 60)
        
        # Pour la démo, on va scanner les plages configurées
        all_hosts = []
        
        for network in self.audit_config.get('network_ranges', []):
            print(f"\n  🔍 Scan de {network}...")
            
            if NMAP_AVAILABLE:
                hosts = self._scan_with_nmap(network)
            else:
                hosts = self._scan_basic(network)
            
            all_hosts.extend(hosts)
        
        print(f"\n  📊 Total: {len(all_hosts)} hôtes détectés")
        
        # Analyse EOL
        print("\n  🔍 Analyse des dates de fin de vie...")
        
        eol_report = []
        warning_threshold = self.audit_config.get('alert_thresholds', {}).get('eol_warning_days', 180)
        critical_threshold = self.audit_config.get('alert_thresholds', {}).get('eol_critical_days', 90)
        
        for host in all_hosts:
            eol_info = self._check_eol_status(host.get('os', 'Unknown'), host.get('version', 'Unknown'))
            
            report_entry = {
                **host,
                **eol_info
            }
            
            eol_report.append(report_entry)
        
        # Statistiques
        eol_count = sum(1 for h in eol_report if h.get('eol_status') == 'EOL')
        critical_count = sum(1 for h in eol_report if h.get('eol_status') == 'CRITICAL')
        warning_count = sum(1 for h in eol_report if h.get('eol_status') == 'WARNING')
        active_count = sum(1 for h in eol_report if h.get('eol_status') == 'ACTIVE')
        unknown_count = sum(1 for h in eol_report if h.get('eol_status') == 'UNKNOWN')
        
        print(f"\n📊 Analyse:")
        print(f"  🔴 EOL (fin de vie): {eol_count}")
        print(f"  🟠 Critique (<{critical_threshold} jours): {critical_count}")
        print(f"  🟡 Avertissement (<{warning_threshold} jours): {warning_count}")
        print(f"  🟢 Actif: {active_count}")
        print(f"  ⚪ Inconnu: {unknown_count}")
        
        # Sauvegarde
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # JSON
        json_file = self.output_dir / f"eol_report_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'report_date': datetime.now().isoformat(),
                'total_hosts': len(eol_report),
                'statistics': {
                    'eol': eol_count,
                    'critical': critical_count,
                    'warning': warning_count,
                    'active': active_count,
                    'unknown': unknown_count
                },
                'hosts': eol_report
            }, f, indent=2, ensure_ascii=False)
        
        # CSV
        csv_file = self.output_dir / f"eol_report_{timestamp}.csv"
        if eol_report:
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                fieldnames = list(eol_report[0].keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                writer.writerows(eol_report)
        
        print(f"\n💾 Rapports générés:")
        print(f"  • JSON: {json_file.name}")
        print(f"  • CSV: {csv_file.name}")
        
        self.logger.info(f"Rapport EOL généré: {len(eol_report)} hôtes analysés")
        
        return True
    
    def check_os_eol(self, os_name, version):
        """
        Vérifie la fin de vie d'un OS spécifique
        
        Args:
            os_name: Nom de l'OS
            version: Version
        
        Returns:
            bool: True si trouvé
        """
        print(f"\n🔍 Vérification EOL: {os_name} {version}")
        print("─" * 60)
        
        eol_info = self._check_eol_status(os_name, version)
        
        if eol_info['eol_status'] == 'UNKNOWN':
            print(f"  ⚠️  OS non trouvé dans la base de données")
            return False
        
        print(f"\n📊 Informations:")
        print(f"  • OS: {os_name} {version}")
        print(f"  • Statut: {eol_info['eol_status']}")
        
        if eol_info.get('eol_date'):
            print(f"  • Date EOL: {eol_info['eol_date']}")
        
        if eol_info.get('days_until_eol'):
            days = eol_info['days_until_eol']
            if days > 0:
                print(f"  • Jours restants: {days}")
            else:
                print(f"  • Expiré depuis: {abs(days)} jours")
        
        return True
    
    def _check_eol_status(self, os_name, version):
        """Vérifie le statut EOL d'un OS"""
        result = {
            'eol_status': 'UNKNOWN',
            'eol_date': None,
            'days_until_eol': None
        }
        
        # Recherche dans la base EOL
        if os_name in self.eol_database:
            os_versions = self.eol_database[os_name]
            
            if version in os_versions:
                version_info = os_versions[version]
                eol_date_str = version_info.get('eol_date')
                
                if eol_date_str:
                    result['eol_date'] = eol_date_str
                    
                    try:
                        eol_date = datetime.strptime(eol_date_str, '%Y-%m-%d')
                        today = datetime.now()
                        days_until = (eol_date - today).days
                        
                        result['days_until_eol'] = days_until
                        
                        # Déterminer le statut
                        warning_days = self.audit_config.get('alert_thresholds', {}).get('eol_warning_days', 180)
                        critical_days = self.audit_config.get('alert_thresholds', {}).get('eol_critical_days', 90)
                        
                        if days_until < 0:
                            result['eol_status'] = 'EOL'
                        elif days_until < critical_days:
                            result['eol_status'] = 'CRITICAL'
                        elif days_until < warning_days:
                            result['eol_status'] = 'WARNING'
                        else:
                            result['eol_status'] = 'ACTIVE'
                    
                    except ValueError:
                        result['eol_status'] = version_info.get('status', 'UNKNOWN')
        
        return result
