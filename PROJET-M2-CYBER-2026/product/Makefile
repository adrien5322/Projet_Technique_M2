.PHONY: help setup build up down logs test lint clean

help:
	@echo "DAR-Cyber - Commandes disponibles:"
	@echo ""
	@echo "Setup:"
	@echo "  setup       - Configuration initiale du projet"
	@echo "  build       - Construire les images Docker"
	@echo ""
	@echo "Développement:"
	@echo "  up          - Démarrer les services (mode détaché)"
	@echo "  down        - Arrêter les services"
	@echo "  logs        - Voir les logs (suivi)"
	@echo "  restart     - Redémarrer les services"
	@echo ""
	@echo "Tests et Qualité:"
	@echo "  test        - Exécuter les tests"
	@echo "  lint        - Vérifier le code (flake8)"
	@echo "  format      - Formater le code (black, isort)"
	@echo ""
	@echo "Base de données:"
	@echo "  db-up       - Appliquer les migrations (alembic upgrade head)"
	@echo "  db-down     - Annuler la dernière migration"
	@echo "  db-reset    - Reset complet de la base (⚠️ supprime les données)"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean       - Nettoyer les conteneurs et volumes inutilisés"
	@echo "  ps          - Voir l'état des services"

setup:
	@echo "🔧 Configuration initiale..."
	./scripts/setup.sh

build:
	@echo "🔨 Construction des images Docker..."
	docker compose build

up:
	@echo "🚀 Démarrage des services..."
	docker compose up -d
	@echo "✓ Services démarrés. Logs: make logs"

down:
	@echo "⏹️  Arrêt des services..."
	docker compose down

logs:
	docker compose logs -f

restart:
	@echo "🔄 Redémarrage des services..."
	docker compose restart

test:
	@echo "🧪 Exécution des tests..."
	docker compose run --rm backend pytest tests/ -v

test-cov:
	@echo "🧪 Exécution des tests avec couverture..."
	docker compose run --rm backend pytest tests/ --cov=app --cov-report=html

lint:
	@echo "🔍 Vérification du code..."
	docker compose run --rm backend flake8 app/

format:
	@echo "🎨 Formatage du code..."
	docker compose run --rm backend black app/
	docker compose run --rm backend isort app/

db-up:
	@echo "⬆️  Migration de la base de données..."
	docker compose run --rm backend alembic upgrade head

db-down:
	@echo "⬇️  Annulation de la dernière migration..."
	docker compose run --rm backend alembic downgrade -1

db-reset:
	@echo "⚠️  Reset de la base de données..."
	docker compose down -v
	docker compose up -d postgres redis
	@sleep 5
	docker compose run --rm backend alembic upgrade head

clean:
	@echo "🧹 Nettoyage..."
	docker compose down -v --remove-orphans
	docker system prune -f

ps:
	docker compose ps

shell:
	@echo "🐚 Shell dans le conteneur backend..."
	docker compose exec backend bash

pg-shell:
	@echo "🐘 Shell PostgreSQL..."
	docker compose exec postgres psql -U devinciwatch

help-internal:
	@echo "Variables d'environnement actuelles:"
	@cat backend/.env 2>/dev/null || echo "Fichier .env non trouvé"
