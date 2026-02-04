#!/usr/bin/env python3
"""
Utilitaire de configuration du système de logging
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(name='NTL-SysToolbox', level='INFO', log_to_file=True):
    """
    Configure et retourne un logger
    
    Args:
        name: Nom du logger
        level: Niveau de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Si True, log aussi dans un fichier
    
    Returns:
        logging.Logger: Logger configuré
    """
    logger = logging.getLogger(name)
    
    # Éviter de dupliquer les handlers
    if logger.handlers:
        return logger
    
    # Niveau de log
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Format des messages
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler fichier si demandé
    if log_to_file:
        try:
            # Créer le dossier de logs
            log_dir = Path(__file__).parent.parent.parent / 'outputs' / 'logs'
            log_dir.mkdir(parents=True, exist_ok=True)
            
            # Nom du fichier avec timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_file = log_dir / f'ntl_systoolbox_{timestamp}.log'
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
            logger.info(f"Logs sauvegardés dans: {log_file}")
        
        except Exception as e:
            logger.warning(f"Impossible de créer le fichier de log: {e}")
    
    return logger


def get_logger(name=None):
    """
    Récupère un logger existant ou en crée un nouveau
    
    Args:
        name: Nom du logger (None pour le logger root)
    
    Returns:
        logging.Logger: Logger
    """
    if name:
        return logging.getLogger(name)
    return logging.getLogger('NTL-SysToolbox')
