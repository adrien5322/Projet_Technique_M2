#!/usr/bin/env python3
"""
Script de validation de la structure DAR-Cyber Backend.
Vérifie que tous les fichiers sont présents et que la syntaxe est correcte.
"""

import os
import sys
import py_compile
from pathlib import Path

# Couleurs pour l'affichage
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def print_status(message, status):
    """Affiche un message avec un statut coloré."""
    if status:
        print(f"{GREEN}✓{RESET} {message}")
    else:
        print(f"{RED}✗{RESET} {message}")

def check_file_exists(filepath):
    """Vérifie si un fichier existe."""
    return os.path.isfile(filepath)

def check_syntax(filepath):
    """Vérifie la syntaxe d'un fichier Python."""
    try:
        py_compile.compile(filepath, doraise=True)
        return True
    except py_compile.PyCompileError:
        return False

def main():
    print("=" * 60)
    print("DAR-Cyber Backend - Validation de la structure")
    print("=" * 60)
    print()
    
    backend_dir = Path(__file__).parent
    
    # Fichiers requis
    required_files = [
        "app/__init__.py",
        "app/main.py",
        "app/config.py",
        "app/models/__init__.py",
        "app/models/user.py",
        "app/schemas/__init__.py",
        "app/schemas/user.py",
        "app/auth/__init__.py",
        "app/auth/service.py",
        "app/auth/routes.py",
        "app/auth/dependencies.py",
        "app/core/__init__.py",
        "app/core/health.py",
        "requirements.txt",
        ".env.example",
        "README.md",
    ]
    
    # Vérification des fichiers
    print("📁 Vérification des fichiers :")
    all_files_exist = True
    for file in required_files:
        filepath = backend_dir / file
        exists = check_file_exists(filepath)
        print_status(file, exists)
        if not exists:
            all_files_exist = False
    
    print()
    
    # Vérification de la syntaxe Python
    print("🔍 Vérification de la syntaxe Python :")
    python_files = [
        "app/__init__.py",
        "app/main.py",
        "app/config.py",
        "app/models/user.py",
        "app/schemas/user.py",
        "app/auth/service.py",
        "app/auth/routes.py",
        "app/auth/dependencies.py",
        "app/core/health.py",
    ]
    
    all_syntax_ok = True
    for file in python_files:
        filepath = backend_dir / file
        if check_file_exists(filepath):
            syntax_ok = check_syntax(filepath)
            print_status(f"Syntaxe: {file}", syntax_ok)
            if not syntax_ok:
                all_syntax_ok = False
    
    print()
    
    # Résumé
    print("=" * 60)
    print("RÉSUMÉ")
    print("=" * 60)
    
    if all_files_exist:
        print(f"{GREEN}✓ Tous les fichiers requis sont présents{RESET}")
    else:
        print(f"{RED}✗ Certains fichiers sont manquants{RESET}")
    
    if all_syntax_ok:
        print(f"{GREEN}✓ Tous les fichiers Python ont une syntaxe correcte{RESET}")
    else:
        print(f"{RED}✗ Erreurs de syntaxe détectées{RESET}")
    
    print()
    print(f"{YELLOW}ℹ Pour installer les dépendances :{RESET}")
    print("  1. Installer python3-pip et python3-venv (sudo apt-get install python3-pip python3-venv)")
    print("  2. ./setup.sh")
    print("  3. source venv/bin/activate")
    print("  4. uvicorn app.main:app --reload")
    
    return 0 if (all_files_exist and all_syntax_ok) else 1

if __name__ == "__main__":
    sys.exit(main())
