PIPENV=PIPENV_VENV_IN_PROJECT=1 pipenv
PIPENV_RUN=$(PIPENV) run
SOURCES_FOLDER=./send_to_kindle

SOURCE_FILES=$(shell find . -name *.py -not -path **/.venv/*)

env:
	$(PIPENV) install --dev

test:
	$(PIPENV_RUN) pytest --cov=$(SOURCES_FOLDER) tests

format:
	$(PIPENV_RUN) isort -rc $(SOURCES_FOLDER)
	$(PIPENV_RUN) black $(SOURCE_FILES)

lint:
	$(PIPENV_RUN) bandit -r $(SOURCES_FOLDER)
	$(PIPENV_RUN) isort -rc $(SOURCES_FOLDER) --check-only
	$(PIPENV_RUN) black $(SOURCE_FILES) --check
	$(PIPENV_RUN) pylint $(SOURCES_FOLDER)
