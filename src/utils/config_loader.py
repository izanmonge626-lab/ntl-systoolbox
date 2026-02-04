#!/usr/bin/env python3
"""
Utilitaire de chargement et validation de la configuration
"""

import json
import os
from pathlib import Path


def load_config(config_path='config/config.json'):
    """
    Charge le fichier de configuration JSON
    
    Args:
        config_path: Chemin vers le fichier de configuration
    
    Returns:
        dict: Configuration chargée
    
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        json.JSONDecodeError: Si le JSON est invalide
    """
    # Gestion des chemins relatifs
    if not os.path.isabs(config_path):
        # Cherche depuis le dossier parent de src/
        base_dir = Path(__file__).parent.parent
        config_path = base_dir / config_path
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Fichier de configuration introuvable: {config_path}\n"
            "💡 Copiez config/config.example.json vers config/config.json"
        )
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Validation basique
    validate_config(config)
    
    # Surcharge par variables d'environnement si présentes
    config = override_with_env(config)
    
    return config


def validate_config(config):
    """
    Valide la structure de base de la configuration
    
    Args:
        config: Configuration à valider
    
    Raises:
        ValueError: Si la configuration est invalide
    """
    required_sections = ['general', 'diagnostic', 'backup', 'audit']
    
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Section '{section}' manquante dans la configuration")
    
    # Validation section général
    general = config['general']
    if 'output_dir' not in general:
        raise ValueError("'output_dir' manquant dans la section 'general'")
    
    # Validation section diagnostic
    diagnostic = config['diagnostic']
    if 'mysql_servers' not in diagnostic:
        raise ValueError("'mysql_servers' manquant dans la section 'diagnostic'")
    
    # Validation section backup
    backup = config['backup']
    if 'mysql' not in backup:
        raise ValueError("'mysql' manquant dans la section 'backup'")
    
    # Validation section audit
    audit = config['audit']
    if 'network_ranges' not in audit:
        raise ValueError("'network_ranges' manquant dans la section 'audit'")
    if 'eol_database_file' not in audit:
        raise ValueError("'eol_database_file' manquant dans la section 'audit'")


def override_with_env(config):
    """
    Surcharge certains paramètres avec des variables d'environnement
    
    Variables supportées:
        NTL_MYSQL_HOST: Host MySQL
        NTL_MYSQL_USER: Utilisateur MySQL
        NTL_MYSQL_PASSWORD: Mot de passe MySQL
        NTL_LOG_LEVEL: Niveau de log
    
    Args:
        config: Configuration de base
    
    Returns:
        dict: Configuration avec surcharges
    """
    # MySQL
    if os.getenv('NTL_MYSQL_HOST'):
        config['backup']['mysql']['host'] = os.getenv('NTL_MYSQL_HOST')
    if os.getenv('NTL_MYSQL_USER'):
        config['backup']['mysql']['username'] = os.getenv('NTL_MYSQL_USER')
    if os.getenv('NTL_MYSQL_PASSWORD'):
        config['backup']['mysql']['password'] = os.getenv('NTL_MYSQL_PASSWORD')
    
    # Log level
    if os.getenv('NTL_LOG_LEVEL'):
        config['general']['log_level'] = os.getenv('NTL_LOG_LEVEL')
    
    return config


def get_output_dir(config):
    """
    Retourne le chemin du répertoire de sortie
    
    Args:
        config: Configuration
    
    Returns:
        Path: Chemin du répertoire de sortie
    """
    output_dir = config['general']['output_dir']
    
    if not os.path.isabs(output_dir):
        base_dir = Path(__file__).parent.parent
        output_dir = base_dir / output_dir
    
    return Path(output_dir)


def ensure_output_dirs(config):
    """
    Crée les répertoires de sortie s'ils n'existent pas
    
    Args:
        config: Configuration
    """
    output_dir = get_output_dir(config)
    
    dirs_to_create = [
        output_dir,
        output_dir / 'logs',
        output_dir / 'backups',
        output_dir / 'reports'
    ]
    
    for directory in dirs_to_create:
        directory.mkdir(parents=True, exist_ok=True)
