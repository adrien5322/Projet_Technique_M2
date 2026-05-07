#!/bin/bash
# Script de démarrage pour DAR-Cyber
# Usage: ./scripts/start.sh [--build] [--detach]

set -e

# Couleurs pour les messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Répertoire du projet
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Vérification de Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Erreur: Docker n'est pas installé${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}Erreur: Docker Compose n'est pas installé${NC}"
    exit 1
fi

# Vérification du fichier .env
if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}Attention: Le fichier backend/.env n'existe pas${NC}"
    echo -e "${YELLOW}Copie de backend/.env.example vers backend/.env${NC}"
    cp backend/.env.example backend/.env
    echo -e "${GREEN}Fichier .env créé. Vous pouvez le modifier si nécessaire.${NC}"
fi

# Parsing des arguments
BUILD_FLAG=""
DETACH_FLAG=""

for arg in "$@"; do
    case $arg in
        --build)
            BUILD_FLAG="--build"
            shift
            ;;
        --detach|-d)
            DETACH_FLAG="-d"
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --build       Reconstruit les images Docker"
            echo "  --detach, -d  Lance les conteneurs en arrière-plan"
            echo "  --help, -h    Affiche cette aide"
            exit 0
            ;;
        *)
            echo -e "${RED}Argument inconnu: $arg${NC}"
            exit 1
            ;;
    esac
done

echo -e "${GREEN}=== Démarrage de DAR-Cyber ===${NC}"

# Arrêt des conteneurs existants
echo -e "${YELLOW}Arrêt des conteneurs existants...${NC}"
docker compose down 2>/dev/null || true

# Démarrage des services
echo -e "${GREEN}Démarrage des services...${NC}"
if [ -n "$BUILD_FLAG" ]; then
    echo -e "${YELLOW}Construction des images...${NC}"
fi

docker compose up $BUILD_FLAG $DETACH_FLAG

# Si lancé en mode attaché, on affiche les logs
if [ -z "$DETACH_FLAG" ]; then
    echo -e "${GREEN}Services démarrés. Utilisez Ctrl+C pour arrêter.${NC}"
fi
