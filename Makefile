
current_dir := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

# Up & Down

run-mysql:
	docker-compose -f infra/docker-compose.yml up -d --remove-orphans mysql

run: run-mysql

stop:
	docker-compose -f infra/docker-compose.yml stop

