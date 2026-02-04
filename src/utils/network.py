#!/usr/bin/env python3
"""
Utilitaires réseau pour validation et manipulation d'adresses
"""

import socket
import ipaddress
import subprocess
import platform


def is_valid_ip(ip):
    """
    Vérifie si une chaîne est une adresse IP valide
    
    Args:
        ip: Chaîne à vérifier
    
    Returns:
        bool: True si IP valide
    """
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def is_valid_network(network):
    """
    Vérifie si une chaîne est une plage réseau valide (CIDR)
    
    Args:
        network: Chaîne à vérifier (ex: 192.168.1.0/24)
    
    Returns:
        bool: True si réseau valide
    """
    try:
        ipaddress.ip_network(network, strict=False)
        return True
    except ValueError:
        return False


def ping_host(host, timeout=2):
    """
    Ping un hôte pour vérifier s'il est accessible
    
    Args:
        host: IP ou hostname à pinger
        timeout: Timeout en secondes
    
    Returns:
        bool: True si l'hôte répond
    """
    # Paramètres selon l'OS
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    timeout_param = '-w' if platform.system().lower() == 'windows' else '-W'
    
    command = ['ping', param, '1', timeout_param, str(timeout), host]
    
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout + 1
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, Exception):
        return False


def resolve_hostname(hostname):
    """
    Résout un hostname en adresse IP
    
    Args:
        hostname: Nom d'hôte à résoudre
    
    Returns:
        str|None: Adresse IP ou None si échec
    """
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None


def get_network_hosts(network):
    """
    Génère la liste des hôtes d'un réseau
    
    Args:
        network: Réseau en notation CIDR (ex: 192.168.1.0/24)
    
    Returns:
        list: Liste des adresses IP du réseau
    """
    try:
        net = ipaddress.ip_network(network, strict=False)
        # Exclure l'adresse réseau et broadcast
        return [str(ip) for ip in net.hosts()]
    except ValueError:
        return []


def check_port(host, port, timeout=2):
    """
    Vérifie si un port est ouvert sur un hôte
    
    Args:
        host: IP ou hostname
        port: Numéro de port
        timeout: Timeout en secondes
    
    Returns:
        bool: True si le port est ouvert
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    
    try:
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except socket.error:
        return False


def get_local_ip():
    """
    Récupère l'adresse IP locale de la machine
    
    Returns:
        str: Adresse IP locale
    """
    try:
        # Astuce: se connecter à une IP externe sans vraiment envoyer de données
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"


def format_mac_address(mac):
    """
    Formate une adresse MAC au format standard
    
    Args:
        mac: Adresse MAC (divers formats)
    
    Returns:
        str: MAC formatée (XX:XX:XX:XX:XX:XX)
    """
    # Supprimer tous les séparateurs
    mac = mac.replace(':', '').replace('-', '').replace('.', '')
    
    # Vérifier la longueur
    if len(mac) != 12:
        return mac
    
    # Reformater
    return ':'.join(mac[i:i+2] for i in range(0, 12, 2)).upper()
