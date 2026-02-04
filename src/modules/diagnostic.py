#!/usr/bin/env python3
"""
Module 1 - Diagnostic
Vérification des services critiques et état des serveurs
"""

import json
import mysql.connector
from datetime import datetime
from pathlib import Path
import psutil
import platform

try:
    import winrm
    WINRM_AVAILABLE = True
except ImportError:
    WINRM_AVAILABLE = False

try:
    import paramiko
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False


class DiagnosticModule:
    """Module de diagnostic système"""
    
    def __init__(self, config, logger):
        """
        Initialise le module de diagnostic
        
        Args:
            config: Configuration chargée
            logger: Logger configuré
        """
        self.config = config
        self.logger = logger
        self.diagnostic_config = config.get('diagnostic', {})
        self.output_dir = Path(config['general']['output_dir']) / 'reports'
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def check_mysql(self):
        """
        Vérifie la connexion et l'état des serveurs MySQL
        
        Returns:
            bool: True si tous les serveurs sont OK
        """
        self.logger.info("=== Début vérification MySQL ===")
        print("\n📊 Vérification des serveurs MySQL")
        print("─" * 60)
        
        mysql_servers = self.diagnostic_config.get('mysql_servers', [])
        
        if not mysql_servers:
            self.logger.warning("Aucun serveur MySQL configuré")
            print("⚠️  Aucun serveur MySQL configuré")
            return False
        
        all_ok = True
        results = []
        
        for server in mysql_servers:
            name = server.get('name', 'Unknown')
            host = server.get('ip', server.get('host', 'localhost'))
            port = server.get('port', 3306)
            user = server.get('username', 'root')
            password = server.get('password', '')
            database = server.get('database', None)
            
            print(f"\n🔍 Test de {name} ({host}:{port})...")
            
            result = {
                'server': name,
                'host': host,
                'port': port,
                'timestamp': datetime.now().isoformat(),
                'status': 'unknown'
            }
            
            try:
                # Tentative de connexion
                conn = mysql.connector.connect(
                    host=host,
                    port=port,
                    user=user,
                    password=password,
                    database=database,
                    connect_timeout=5
                )
                
                cursor = conn.cursor()
                
                # Test basique
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()[0]
                result['version'] = version
                
                # Test de performance
                start_time = datetime.now()
                cursor.execute("SELECT 1")
                cursor.fetchone()
                response_time = (datetime.now() - start_time).total_seconds() * 1000
                result['response_time_ms'] = round(response_time, 2)
                
                # Nombre de connexions actives
                cursor.execute("SHOW STATUS LIKE 'Threads_connected'")
                threads = cursor.fetchone()[1]
                result['active_connections'] = int(threads)
                
                # Uptime
                cursor.execute("SHOW STATUS LIKE 'Uptime'")
                uptime_seconds = int(cursor.fetchone()[1])
                uptime_hours = uptime_seconds / 3600
                result['uptime_hours'] = round(uptime_hours, 2)
                
                cursor.close()
                conn.close()
                
                result['status'] = 'OK'
                print(f"  ✅ Connexion réussie")
                print(f"  📌 Version: {version}")
                print(f"  ⏱️  Temps de réponse: {result['response_time_ms']} ms")
                print(f"  🔗 Connexions actives: {result['active_connections']}")
                print(f"  ⏰ Uptime: {result['uptime_hours']} heures")
                
                self.logger.info(f"MySQL {name} OK - Version {version}")
            
            except mysql.connector.Error as e:
                result['status'] = 'ERROR'
                result['error'] = str(e)
                print(f"  ❌ Erreur: {e}")
                self.logger.error(f"MySQL {name} ERREUR: {e}")
                all_ok = False
            
            except Exception as e:
                result['status'] = 'ERROR'
                result['error'] = str(e)
                print(f"  ❌ Erreur inattendue: {e}")
                self.logger.error(f"MySQL {name} ERREUR INATTENDUE: {e}")
                all_ok = False
            
            results.append(result)
        
        # Sauvegarde du résultat
        self._save_results('mysql_check', results)
        
        print("\n" + "─" * 60)
        if all_ok:
            print("✅ Tous les serveurs MySQL sont opérationnels")
            return True
        else:
            print("❌ Certains serveurs MySQL ont des problèmes")
            return False
    
    def check_ad_dns(self):
        """
        Vérifie les services AD et DNS sur les contrôleurs de domaine
        
        Returns:
            bool: True si tous les services sont OK
        """
        self.logger.info("=== Début vérification AD/DNS ===")
        print("\n📊 Vérification des services AD/DNS")
        print("─" * 60)
        
        ad_servers = self.diagnostic_config.get('ad_dns_servers', [])
        
        if not ad_servers:
            self.logger.warning("Aucun serveur AD/DNS configuré")
            print("⚠️  Aucun serveur AD/DNS configuré")
            return False
        
        all_ok = True
        results = []
        
        for server in ad_servers:
            name = server.get('name', 'Unknown')
            ip = server.get('ip', '')
            services = server.get('services_to_check', ['DNS', 'ActiveDirectory'])
            
            print(f"\n🔍 Vérification de {name} ({ip})...")
            
            result = {
                'server': name,
                'ip': ip,
                'timestamp': datetime.now().isoformat(),
                'services': {}
            }
            
            # Pour l'instant, vérification basique (ping + port)
            from utils.network import ping_host, check_port
            
            # Test de connectivité
            if ping_host(ip):
                print(f"  ✅ Serveur accessible (ping)")
                result['reachable'] = True
                
                # Test ports DNS (53) et AD (389 LDAP)
                dns_ok = check_port(ip, 53)
                ldap_ok = check_port(ip, 389)
                
                result['services']['DNS'] = 'OK' if dns_ok else 'DOWN'
                result['services']['LDAP'] = 'OK' if ldap_ok else 'DOWN'
                
                if dns_ok:
                    print(f"  ✅ Service DNS (port 53) actif")
                else:
                    print(f"  ❌ Service DNS (port 53) inactif")
                    all_ok = False
                
                if ldap_ok:
                    print(f"  ✅ Service LDAP (port 389) actif")
                else:
                    print(f"  ❌ Service LDAP (port 389) inactif")
                    all_ok = False
            
            else:
                print(f"  ❌ Serveur injoignable")
                result['reachable'] = False
                result['services'] = {s: 'UNKNOWN' for s in services}
                all_ok = False
            
            results.append(result)
        
        # Sauvegarde du résultat
        self._save_results('ad_dns_check', results)
        
        print("\n" + "─" * 60)
        if all_ok:
            print("✅ Tous les services AD/DNS sont opérationnels")
            return True
        else:
            print("❌ Certains services AD/DNS ont des problèmes")
            return False
    
    def get_server_info(self, target_ip, os_type='auto'):
        """
        Récupère les informations d'un serveur (version OS, uptime, ressources)
        
        Args:
            target_ip: IP du serveur cible
            os_type: Type d'OS ('windows', 'linux', 'auto')
        
        Returns:
            bool: True si succès
        """
        self.logger.info(f"=== Collecte d'infos serveur {target_ip} ===")
        print(f"\n📊 Informations du serveur {target_ip}")
        print("─" * 60)
        
        result = {
            'server': target_ip,
            'timestamp': datetime.now().isoformat(),
            'os_type': os_type
        }
        
        # Si c'est la machine locale
        from utils.network import get_local_ip
        local_ip = get_local_ip()
        
        if target_ip in ['localhost', '127.0.0.1', local_ip]:
            print("  ℹ️  Détection: Machine locale")
            return self._get_local_server_info(result)
        
        # Sinon tentative connexion distante
        else:
            print("  ℹ️  Tentative de connexion distante...")
            # Pour l'instant, version simplifiée
            print("  ⚠️  Connexion distante non encore implémentée")
            print("  💡 Utilisez cette fonctionnalité sur la machine cible")
            return False
    
    def _get_local_server_info(self, result):
        """Récupère les infos de la machine locale"""
        try:
            # Version OS
            os_info = platform.uname()
            result['os'] = {
                'system': os_info.system,
                'release': os_info.release,
                'version': os_info.version,
                'machine': os_info.machine,
                'processor': os_info.processor
            }
            
            print(f"\n💻 Système d'exploitation:")
            print(f"  • OS: {os_info.system} {os_info.release}")
            print(f"  • Version: {os_info.version}")
            print(f"  • Architecture: {os_info.machine}")
            
            # Uptime
            import time
            boot_time = psutil.boot_time()
            uptime_seconds = time.time() - boot_time
            uptime_hours = uptime_seconds / 3600
            result['uptime_hours'] = round(uptime_hours, 2)
            
            print(f"\n⏰ Uptime: {uptime_hours:.2f} heures")
            
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            result['cpu'] = {
                'usage_percent': cpu_percent,
                'count': cpu_count
            }
            
            print(f"\n🔧 Processeur:")
            print(f"  • Utilisation: {cpu_percent}%")
            print(f"  • Cœurs: {cpu_count}")
            
            # RAM
            memory = psutil.virtual_memory()
            result['memory'] = {
                'total_gb': round(memory.total / (1024**3), 2),
                'used_gb': round(memory.used / (1024**3), 2),
                'available_gb': round(memory.available / (1024**3), 2),
                'percent': memory.percent
            }
            
            print(f"\n💾 Mémoire RAM:")
            print(f"  • Total: {result['memory']['total_gb']} GB")
            print(f"  • Utilisée: {result['memory']['used_gb']} GB ({memory.percent}%)")
            print(f"  • Disponible: {result['memory']['available_gb']} GB")
            
            # Disques
            disks = []
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_info = {
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'fstype': partition.fstype,
                        'total_gb': round(usage.total / (1024**3), 2),
                        'used_gb': round(usage.used / (1024**3), 2),
                        'free_gb': round(usage.free / (1024**3), 2),
                        'percent': usage.percent
                    }
                    disks.append(disk_info)
                except PermissionError:
                    continue
            
            result['disks'] = disks
            
            print(f"\n💿 Disques:")
            for disk in disks:
                print(f"  • {disk['mountpoint']} ({disk['device']})")
                print(f"    Total: {disk['total_gb']} GB | Utilisé: {disk['used_gb']} GB ({disk['percent']}%)")
            
            # Sauvegarde
            self._save_results('server_info', [result])
            
            print("\n" + "─" * 60)
            print("✅ Informations collectées avec succès")
            
            return True
        
        except Exception as e:
            self.logger.error(f"Erreur collecte infos: {e}")
            print(f"\n❌ Erreur: {e}")
            return False
    
    def _save_results(self, check_type, results):
        """Sauvegarde les résultats en JSON"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{check_type}_{timestamp}.json"
        filepath = self.output_dir / filename
        
        output = {
            'check_type': check_type,
            'timestamp': datetime.now().isoformat(),
            'results': results
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Résultats sauvegardés: {filepath}")
        print(f"\n💾 Rapport sauvegardé: {filepath}")
