#!/bin/bash
# Script d'initialisation pour DAR-Cyber
# Usage: ./scripts/setup.sh

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

echo -e "${GREEN}=== Configuration initiale de DAR-Cyber ===${NC}"

# 1. Vérification des prérequis
echo -e "${YELLOW}1. Vérification des prérequis...${NC}"

if ! command -v docker &> /dev/null; then
    echo -e "${RED}Erreur: Docker n'est pas installé${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}Erreur: Docker Compose n'est pas installé${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker et Docker Compose sont installés${NC}"

# 2. Configuration du fichier .env
echo -e "${YELLOW}2. Configuration des variables d'environnement...${NC}"

if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}Création du fichier backend/.env à partir de .env.example${NC}"
    cp backend/.env.example backend/.env
    echo -e "${GREEN}✓ Fichier .env créé${NC}"
    echo -e "${YELLOW}Pensez à modifier les valeurs dans backend/.env si nécessaire${NC}"
else
    echo -e "${GREEN}✓ Le fichier backend/.env existe déjà${NC}"
fi

# 3. Construction des images Docker
echo -e "${YELLOW}3. Construction des images Docker...${NC}"
docker compose build
echo -e "${GREEN}✓ Images Docker construites${NC}"

# 4. Démarrage des services de base de données
echo -e "${YELLOW}4. Démarrage des services de base de données...${NC}"
docker compose up -d postgres redis
echo -e "${YELLOW}Attente que les services soient prêts...${NC}"

# Attendre que PostgreSQL soit prêt
echo -e "${YELLOW}Attente de PostgreSQL...${NC}"
timeout=60
counter=0
until docker exec devinciwatch-postgres pg_isready -U devinciwatch 2>/dev/null; do
    sleep 1
    counter=$((counter + 1))
    if [ $counter -ge $timeout ]; then
        echo -e "${RED}Timeout: PostgreSQL n'est pas prêt après ${timeout}s${NC}"
        exit 1
    fi
done
echo -e "${GREEN}✓ PostgreSQL est prêt${NC}"

# Attendre que Redis soit prêt
echo -e "${YELLOW}Attente de Redis...${NC}"
counter=0
until docker exec devinciwatch-redis redis-cli ping 2>/dev/null | grep -q PONG; do
    sleep 1
    counter=$((counter + 1))
    if [ $counter -ge $timeout ]; then
        echo -e "${RED}Timeout: Redis n'est pas prêt après ${timeout}s${NC}"
        exit 1
    fi
done
echo -e "${GREEN}✓ Redis est prêt${NC}"

# 5. Initialisation de la base de données (migrations Alembic)
echo -e "${YELLOW}5. Initialisation de la base de données...${NC}"
echo -e "${YELLOW}Exécution des migrations Alembic...${NC}"

# Vérifier si Alembic est configuré
if [ -d "backend/alembic" ] && [ -f "backend/alembic.ini" ]; then
    docker compose run --rm backend alembic upgrade head
    echo -e "${GREEN}✓ Migrations de base de données appliquées${NC}"
else
    echo -e "${YELLOW}Attention: Alembic n'est pas encore configuré${NC}"
    echo -e "${YELLOW}Vous devrez configurer Alembic plus tard avec:${NC}"
    echo -e "${YELLOW}  docker compose run --rm backend alembic init alembic${NC}"
fi

# 6. Résumé
echo ""
echo -e "${GREEN}=== Configuration terminée ===${NC}"
echo ""
echo -e "${GREEN}Services configurés:${NC}"
echo "  - PostgreSQL: localhost:5432"
echo "  - Redis: localhost:6379"
echo ""
echo -e "${GREEN}Pour démarrer l'application complète:${NC}"
echo "  ./scripts/start.sh --detach"
echo ""
echo -e "${GREEN}Pour voir les logs:${NC}"
echo "  docker compose logs -f"
echo ""
echo -e "${GREEN}Pour arrêter les services:${NC}"
echo "  docker compose down"
echo ""
