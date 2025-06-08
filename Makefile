build:
	./build.sh

render-start:
	python -m gunicorn task_manager.wsgi

install:
	uv sync

migrate:
	uv run python3 manage.py migrate

start:
	uv run manage.py runserver 0.0.0.0:8000

collectstatic:
	uv run python3 manage.py collectstatic --no-input