PIPENV=PIPENV_VENV_IN_PROJECT=1 pipenv
PIPENV_RUN=$(PIPENV) run
SOURCES_FOLDER=./send_to_kindle

SOURCE_FILES=$(shell find . -name *.py -not -path **/.venv/*)

env:
	$(PIPENV) install --dev

unit_test:
	PYTHONPATH=. $(PIPENV_RUN) pytest -vvv --cov=$(SOURCES_FOLDER) --cov-report=html tests/unit

integration_test:
	PYTHONPATH=. $(PIPENV_RUN) pytest -vvv --cov=$(SOURCES_FOLDER) --cov-report=html tests/integration

format:
	$(PIPENV_RUN) isort -rc $(SOURCES_FOLDER)
	$(PIPENV_RUN) black $(SOURCE_FILES)

lint:
	$(PIPENV_RUN) bandit -r $(SOURCES_FOLDER)
	$(PIPENV_RUN) isort -rc $(SOURCES_FOLDER) --check-only
	$(PIPENV_RUN) black $(SOURCE_FILES) --check
	$(PIPENV_RUN) pylint $(SOURCES_FOLDER)
