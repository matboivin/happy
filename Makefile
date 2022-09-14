COMPOSE = docker-compose -f docker-compose.yml

start:
	poetry run uvicorn --host 127.0.0.1 --reload happy.main:app

up:
	${COMPOSE} up -d

up-build:
	${COMPOSE} up --build -d

stop:
	${COMPOSE} stop

down:
	${COMPOSE} down

status:
	${COMPOSE} ps

logs:
	${COMPOSE} logs

logs-watch:
	${COMPOSE} logs --follow

.PHONY: start up up-build stop down status logs logs-watch
