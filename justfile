default:
    just --list

lint flag="" path=".":
    @ruff check {{flag}} {{path}}

format flag="" path=".":
    @ruff format {{flag}} {{path}}

build:
    @sudo docker build -t forecast-api .

dev:
    @sudo docker run -d -p 5005:80 -w /app -v "$(pwd):/app" forecast-api

start:
    @sudo docker run -d -p 5005:80 forecast-api
