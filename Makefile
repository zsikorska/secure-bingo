up:
	docker-compose up -d

build:
	docker-compose up --build

down:
	docker-compose down

clean:
	docker rmi -f $(shell docker images -aq)
	docker rm -f $(shell docker ps -aq)
	docker ps -a
	docker images -a
