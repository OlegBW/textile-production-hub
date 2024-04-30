default:
    just --list

lint flag="" path=".":
    @ruff check {{flag}} {{path}}

format flag="" path=".":
    @ruff format {{flag}} {{path}}

build:
    @podman build -t textile-production-hub .

dev:
    @podman run --rm -p 5005:5500 -w /app -v "$(pwd):/app" --privileged textile-production-hub
