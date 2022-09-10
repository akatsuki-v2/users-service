#!/usr/bin/make

REPO_DIR = ..

build: # build all containers
	# @docker build -t user-gateway-service:latest $(REPO_DIR)/user-gateway-service
	@docker build -t user-accounts-service:latest $(REPO_DIR)/user-accounts-service

clone: # clone all containers
	# @if [ ! -d $(REPO_DIR)/user-gateway-service ]; then git clone git@github.com:akatsuki-v2/user-gateway-service.git $(REPO_DIR)/user-gateway-service; fi
	@if [ ! -d $(REPO_DIR)/user-accounts-service ]; then git clone git@github.com:akatsuki-v2/user-accounts-service.git $(REPO_DIR)/user-accounts-service; fi

pull: # pull all containers
	# cd $(REPO_DIR)/user-gateway-service && git pull
	cd $(REPO_DIR)/user-accounts-service && git pull

run-bg: # run all containers in the background
	@docker-compose up -d \
		user-accounts-service \
		postgres \
		# user-gateway-service \
		# redis \
		# rabbitmq \
		# elasticsearch \

run: # run all containers in the foreground
	@docker-compose up \
		user-accounts-service \
		postgres \
		# user-gateway-service \
		# redis \
		# rabbitmq \
		# elasticsearch \

logs: # attach to the containers live to view their logs
	@docker-compose logs -f

test: # run the tests
	@docker-compose exec user-accounts-service /scripts/run-tests.sh

test-dbg: # run the tests in debug mode
	@docker-compose exec user-accounts-service /scripts/run-tests.sh --dbg
