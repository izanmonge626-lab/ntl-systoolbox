#!/usr/bin/env python3
"""
Module 2 - Sauvegarde WMS
Gestion des sauvegardes de la base de données MySQL
"""

import json
import subprocess
import csv
from datetime import datetime
from pathlib import Path
import mysql.connector


class BackupModule:
    """Module de sauvegarde de la base WMS"""
    
    def __init__(self, config, logger):
        """
        Initialise le module de sauvegarde
        
        Args:
            config: Configuration chargée
            logger: Logger configuré
        """
        self.config = config
        self.logger = logger
        self.backup_config = config.get('backup', {}).get('mysql', {})
        self.output_dir = Path(config['general']['output_dir']) / 'backups'
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def backup_database(self):
        """
        Effectue une sauvegarde complète de la base de données
        
        Returns:
            bool: True si succès
        """
        self.logger.info("=== Début sauvegarde base de données ===")
        print("\n💾 Sauvegarde complète de la base de données")
        print("─" * 60)
        
        host = self.backup_config.get('host', 'localhost')
        port = self.backup_config.get('port', 3306)
        user = self.backup_config.get('username', 'root')
        password = self.backup_config.get('password', '')
        database = self.backup_config.get('database', 'wms_production')
        
        print(f"  📡 Serveur: {host}:{port}")
        print(f"  🗄️  Base de données: {database}")
        
        # Nom du fichier de sauvegarde
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = self.output_dir / f"backup_{database}_{timestamp}.sql"
        
        try:
            # Tentative avec mysqldump (si disponible)
            print("\n  🔄 Sauvegarde en cours avec mysqldump...")
            
            cmd = [
                'mysqldump',
                f'--host={host}',
                f'--port={port}',
                f'--user={user}',
                f'--password={password}',
                '--single-transaction',
                '--quick',
                '--lock-tables=false',
                database
            ]
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                result = subprocess.run(
                    cmd,
                    stdout=f,
                    stderr=subprocess.PIPE,
                    timeout=300  # 5 minutes max
                )
            
            if result.returncode == 0:
                file_size = backup_file.stat().st_size / (1024 * 1024)  # MB
                print(f"\n  ✅ Sauvegarde réussie")
                print(f"  📁 Fichier: {backup_file.name}")
                print(f"  📊 Taille: {file_size:.2f} MB")
                
                self.logger.info(f"Sauvegarde réussie: {backup_file}")
                
                # Compression si activée
                if self.backup_config.get('compression', {}).get('enabled', False):
                    self._compress_backup(backup_file)
                
                return True
            else:
                error_msg = result.stderr.decode('utf-8')
                print(f"\n  ❌ Erreur mysqldump: {error_msg}")
                self.logger.error(f"Erreur mysqldump: {error_msg}")
                
                # Fallback: sauvegarde Python
                print("\n  🔄 Tentative de sauvegarde alternative...")
                return self._backup_python_method(host, port, user, password, database, backup_file)
        
        except FileNotFoundError:
            print("\n  ⚠️  mysqldump non trouvé, utilisation méthode alternative...")
            return self._backup_python_method(host, port, user, password, database, backup_file)
        
        except subprocess.TimeoutExpired:
            print("\n  ❌ Timeout: la sauvegarde a pris trop de temps")
            self.logger.error("Timeout lors de la sauvegarde")
            return False
        
        except Exception as e:
            print(f"\n  ❌ Erreur: {e}")
            self.logger.error(f"Erreur sauvegarde: {e}")
            return False
    
    def _backup_python_method(self, host, port, user, password, database, backup_file):
        """Méthode de sauvegarde alternative en pur Python"""
        try:
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            
            cursor = conn.cursor()
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                # Header
                f.write(f"-- Sauvegarde NTL-SysToolbox\n")
                f.write(f"-- Base: {database}\n")
                f.write(f"-- Date: {datetime.now().isoformat()}\n\n")
                
                # Liste des tables
                cursor.execute("SHOW TABLES")
                tables = [table[0] for table in cursor.fetchall()]
                
                print(f"  📋 {len(tables)} tables à sauvegarder...")
                
                for table in tables:
                    print(f"    • {table}...", end='', flush=True)
                    
                    # Structure
                    cursor.execute(f"SHOW CREATE TABLE `{table}`")
                    create_statement = cursor.fetchone()[1]
                    f.write(f"\n-- Table: {table}\n")
                    f.write(f"DROP TABLE IF EXISTS `{table}`;\n")
                    f.write(f"{create_statement};\n\n")
                    
                    # Données
                    cursor.execute(f"SELECT * FROM `{table}`")
                    rows = cursor.fetchall()
                    
                    if rows:
                        # Récupérer les noms de colonnes
                        columns = [desc[0] for desc in cursor.description]
                        
                        f.write(f"INSERT INTO `{table}` ({', '.join([f'`{col}`' for col in columns])}) VALUES\n")
                        
                        for i, row in enumerate(rows):
                            values = []
                            for value in row:
                                if value is None:
                                    values.append('NULL')
                                elif isinstance(value, str):
                                    # Échapper les quotes
                                    value = value.replace("'", "''")
                                    values.append(f"'{value}'")
                                elif isinstance(value, (datetime, )):
                                    values.append(f"'{value}'")
                                else:
                                    values.append(str(value))
                            
                            row_sql = f"({', '.join(values)})"
                            
                            if i < len(rows) - 1:
                                f.write(f"{row_sql},\n")
                            else:
                                f.write(f"{row_sql};\n\n")
                    
                    print(" ✓")
            
            cursor.close()
            conn.close()
            
            file_size = backup_file.stat().st_size / (1024 * 1024)
            print(f"\n  ✅ Sauvegarde alternative réussie")
            print(f"  📁 Fichier: {backup_file.name}")
            print(f"  📊 Taille: {file_size:.2f} MB")
            
            self.logger.info(f"Sauvegarde Python réussie: {backup_file}")
            return True
        
        except Exception as e:
            print(f" ✗\n  ❌ Erreur: {e}")
            self.logger.error(f"Erreur sauvegarde Python: {e}")
            return False
    
    def export_table_csv(self, table_name):
        """
        Exporte une table en format CSV
        
        Args:
            table_name: Nom de la table à exporter
        
        Returns:
            bool: True si succès
        """
        self.logger.info(f"=== Export CSV de la table {table_name} ===")
        print(f"\n💾 Export de la table '{table_name}' en CSV")
        print("─" * 60)
        
        host = self.backup_config.get('host', 'localhost')
        port = self.backup_config.get('port', 3306)
        user = self.backup_config.get('username', 'root')
        password = self.backup_config.get('password', '')
        database = self.backup_config.get('database', 'wms_production')
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_file = self.output_dir / f"export_{table_name}_{timestamp}.csv"
        
        try:
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            
            cursor = conn.cursor()
            
            # Vérifier que la table existe
            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            if not cursor.fetchone():
                print(f"  ❌ Table '{table_name}' inexistante dans la base {database}")
                return False
            
            # Récupérer les données
            print(f"  🔄 Extraction des données...")
            cursor.execute(f"SELECT * FROM `{table_name}`")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            
            # Écrire le CSV
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                
                # En-têtes
                writer.writerow(columns)
                
                # Données
                writer.writerows(rows)
            
            cursor.close()
            conn.close()
            
            file_size = csv_file.stat().st_size / 1024  # KB
            print(f"\n  ✅ Export réussi")
            print(f"  📁 Fichier: {csv_file.name}")
            print(f"  📊 {len(rows)} lignes exportées")
            print(f"  📊 Taille: {file_size:.2f} KB")
            
            self.logger.info(f"Export CSV réussi: {csv_file} ({len(rows)} lignes)")
            return True
        
        except mysql.connector.Error as e:
            print(f"\n  ❌ Erreur MySQL: {e}")
            self.logger.error(f"Erreur export CSV: {e}")
            return False
        
        except Exception as e:
            print(f"\n  ❌ Erreur: {e}")
            self.logger.error(f"Erreur export CSV: {e}")
            return False
    
    def _compress_backup(self, backup_file):
        """Compresse un fichier de sauvegarde"""
        try:
            import gzip
            import shutil
            
            compressed_file = Path(str(backup_file) + '.gz')
            
            print(f"\n  🗜️  Compression en cours...")
            
            with open(backup_file, 'rb') as f_in:
                with gzip.open(compressed_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Supprimer le fichier non compressé
            backup_file.unlink()
            
            original_size = backup_file.stat().st_size / (1024 * 1024)
            compressed_size = compressed_file.stat().st_size / (1024 * 1024)
            ratio = (1 - compressed_size / original_size) * 100
            
            print(f"  ✅ Compression réussie")
            print(f"  📊 Taille finale: {compressed_size:.2f} MB (gain: {ratio:.1f}%)")
            
            self.logger.info(f"Compression réussie: {compressed_file}")
        
        except Exception as e:
            print(f"  ⚠️  Erreur compression: {e}")
            self.logger.warning(f"Erreur compression: {e}")
