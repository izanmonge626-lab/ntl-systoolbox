#!/usr/bin/env python3
"""
Module 1 - Diagnostic
- Vérifier MySQL (depuis diagnostic.mysql_servers)
- Vérifier AD/DNS (depuis diagnostic.ad_dns_servers)
- État synthétique machine hôte
"""

import json
import time
from datetime import datetime
from pathlib import Path

import mysql.connector
import platform
import psutil


class DiagnosticModule:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

        output_dir = (
            config.get("general", {}).get("output_dir")
            or config.get("paths", {}).get("outputs")
            or "./outputs"
        )
        self.outputs_dir = Path(output_dir)
        self.reports_dir = self.outputs_dir / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------
    # 1) MYSQL
    # ------------------------------------------------------
    def check_mysql(self):
        print("\n🗄️  Vérification MySQL")
        print("─" * 50)

        diag_cfg = self.config.get("diagnostic", {})
        mysql_servers = diag_cfg.get("mysql_servers", [])

        # Fallback éventuel
        if not mysql_servers:
            mysql_block = self.config.get("mysql", {})
            if mysql_block:
                mysql_servers = [mysql_block]

        if not mysql_servers:
            print("❌ Configuration MySQL absente")
            return False

        # On prend le 1er serveur de la liste (comportement simple)
        cfg = mysql_servers[0]

        # ✅ Mapping compatible avec TON config
        host = cfg.get("host") or cfg.get("ip") or "localhost"
        port = int(cfg.get("port") or 3306)
        user = cfg.get("user") or cfg.get("username")
        password = cfg.get("password")
        database = cfg.get("database")

        if not user or password is None or not database:
            print("❌ Configuration MySQL incomplète (username/password/database)")
            return False

        try:
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
            )

            cursor = conn.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]

            print("✅ Connexion MySQL OK")
            print(f"  • Hôte     : {host}:{port}")
            print(f"  • Base     : {database}")
            print(f"  • Version  : {version}")

            result = {
                "timestamp": datetime.now().isoformat(),
                "status": "OK",
                "host": host,
                "port": port,
                "database": database,
                "version": version,
            }
            self._save_results("mysql_check", [result])

            conn.close()
            return True

        except Exception as e:
            print(f"❌ Erreur MySQL : {e}")
            self.logger.error(f"MySQL error: {e}")
            self._save_results(
                "mysql_check",
                [{
                    "timestamp": datetime.now().isoformat(),
                    "status": "ERROR",
                    "host": host,
                    "port": port,
                    "database": database,
                    "error": str(e),
                }]
            )
            return False

    # ------------------------------------------------------
    # 2) AD / DNS
    # ------------------------------------------------------
    def check_ad_dns(self):
        print("\n🌐 Vérification AD / DNS")
        print("─" * 50)

        diag_cfg = self.config.get("diagnostic", {})
        servers = diag_cfg.get("ad_dns_servers", [])

        # Fallback possible
        if not servers:
            ad_dns_block = self.config.get("ad_dns", {})
            if ad_dns_block:
                servers = (
                    ad_dns_block.get("domain_controllers", [])
                    or ad_dns_block.get("servers", [])
                )

        if not servers:
            print("❌ Aucun contrôleur de domaine configuré")
            return False

        from utils.network import ping_host, check_port

        # Ports AD/DNS “classiques”
        ports = {
            "LDAP": 389,
            "LDAPS": 636,
            "DNS": 53,
            "Kerberos": 88,
            "SMB": 445,
        }

        results = []

        for item in servers:
            # ✅ TON config: chaque entrée est un dict avec ip / name
            if isinstance(item, dict):
                name = item.get("name") or "DC"
                ip = item.get("ip") or item.get("host")
            else:
                # fallback si jamais liste de strings
                name = str(item)
                ip = str(item)

            if not ip:
                continue

            print(f"\n🔍 {name} ({ip})")

            entry = {
                "name": name,
                "ip": ip,
                "timestamp": datetime.now().isoformat(),
                "ping": False,
                "services": {},
            }

            entry["ping"] = ping_host(ip)
            print(f"  • Ping : {'✅' if entry['ping'] else '❌'}")

            for svc, port in ports.items():
                ok = check_port(ip, port)
                entry["services"][svc] = ok
                print(f"  • {svc} ({port}) : {'✅' if ok else '❌'}")

            results.append(entry)

        self._save_results("ad_dns_check", results)
        print("\n✅ Vérification AD / DNS terminée")
        return True

    # ------------------------------------------------------
    # 3) ETAT SYNTHETIQUE MACHINE HOTE
    # ------------------------------------------------------
    def host_synthetic_state(self):
        print("\n🖥️ État synthétique de la machine hôte")
        print("─" * 60)

        data = {
            "timestamp": datetime.now().isoformat(),
            "hostname": platform.node(),
            "os": {},
            "uptime_hours": None,
            "cpu": {},
            "memory": {},
            "disks": [],
        }

        os_info = platform.uname()
        data["os"] = {
            "system": os_info.system,
            "release": os_info.release,
            "version": os_info.version,
            "architecture": os_info.machine,
        }

        print(f"OS : {os_info.system} {os_info.release}")
        print(f"Architecture : {os_info.machine}")

        uptime_h = (time.time() - psutil.boot_time()) / 3600
        data["uptime_hours"] = round(uptime_h, 2)
        print(f"Uptime : {data['uptime_hours']} h")

        data["cpu"] = {
            "usage_percent": psutil.cpu_percent(interval=1),
            "cores": psutil.cpu_count(),
        }
        print(f"CPU : {data['cpu']['usage_percent']} % ({data['cpu']['cores']} cœurs)")

        mem = psutil.virtual_memory()
        data["memory"] = {
            "total_gb": round(mem.total / (1024**3), 2),
            "used_gb": round(mem.used / (1024**3), 2),
            "available_gb": round(mem.available / (1024**3), 2),
            "percent": mem.percent,
        }
        print(f"RAM : {data['memory']['used_gb']} / {data['memory']['total_gb']} GB ({mem.percent} %)")

        print("\nDisques :")
        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                disk = {
                    "mount": part.mountpoint,
                    "fs": part.fstype,
                    "total_gb": round(usage.total / (1024**3), 2),
                    "used_gb": round(usage.used / (1024**3), 2),
                    "free_gb": round(usage.free / (1024**3), 2),
                    "percent": usage.percent,
                }
                data["disks"].append(disk)
                print(f"  • {disk['mount']} : {disk['used_gb']} / {disk['total_gb']} GB ({disk['percent']} %)")
            except PermissionError:
                continue

        self._save_results("host_state", [data])
        print("\n✅ État synthétique généré")
        return True

    # ------------------------------------------------------
    # SAVE JSON
    # ------------------------------------------------------
    def _save_results(self, name, content):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = self.reports_dir / f"{name}_{ts}.json"
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(content, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Rapport généré : {path}")
            return str(path)
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde rapport {name}: {e}")
            return None