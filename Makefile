#!make
include .env
export

test:  ## Run tests
	python -m pytest

build-container:
	docker build . -t ghcr.io/$(GITHUB_USERNAME)/calculatahipotecabot

build: test build-container

start:
	python cli.py

publish: build
	echo $(GITHUB_TOKEN) | docker login ghcr.io -u $(GITHUB_USERNAME) --password-stdin
	docker push ghcr.io/$(GITHUB_USERNAME)/calculatahipotecabot:latest

deploy: publish
	ssh -i $(AWS_KEYS_PATH) $(EC2_INSTANCE) "sudo docker stop calculatahipotecabot || docker rm calculatahipotecabot || true && sudo docker pull ghcr.io/$(GITHUB_USERNAME)/calculatahipotecabot:latest && sudo docker run -d --rm --env-file .env --name calculatahipotecabot ghcr.io/$(GITHUB_USERNAME)/calculatahipotecabot:latest"

undeploy:
	ssh -i $(AWS_KEYS_PATH) $(EC2_INSTANCE) "sudo docker stop calculatahipotecabot || docker rm calculatahipotecabot || true"

all: build publish deploy