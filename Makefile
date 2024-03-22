.PHONY: deps lint shell run binary test test_once typecheck

deps:
	poetry install

lint:
	poetry run ruff check . 

shell:
	poetry run python

run:
	poetry run python app.py $(args)

binary:
	poetry run pyinstaller --onefile -n chair_calculator app.py

test:
	poetry run -- ptw -- -s -vv $(args)

test_once:
	poetry run pytest -s

typecheck:
	poetry run mypy .
