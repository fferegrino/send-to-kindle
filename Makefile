PIPENV=PIPENV_VENV_IN_PROJECT=1 pipenv
PIPENV_RUN=$(PIPENV) run
SOURCES_FOLDER=./send_to_kindle

SOURCE_FILES=$(shell find . -name '*.py' -not -path **/.venv/*)

OSFLAG 				:=
ifeq ($(OS),Windows_NT)
	OSFLAG = WIN
else
	UNAME_S := $(shell uname -s)
	ifeq ($(UNAME_S),Linux)
		OSFLAG = LINUX
	endif
	ifeq ($(UNAME_S),Darwin)
		OSFLAG = OSX
	endif
endif

env:
	$(PIPENV) install --dev

unit_test:
	PYTHONPATH=. $(PIPENV_RUN) pytest -vvv --cov=$(SOURCES_FOLDER) --cov-fail-under=90 --cov-report=html tests/unit

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

kindlegen:
	echo "See this website: https://www.amazon.com/gp/feature.html?ie=UTF8&docId=1000765211"
ifeq ($(OSFLAG),OSX)
	wget -O kindlegen.zip http://kindlegen.s3.amazonaws.com/KindleGen_Mac_i386_v2_9.zip
	unzip kindlegen.zip -d kindlegen
endif
ifeq ($(OSFLAG),LINUX)
	wget -O kindlegen.tar.gz http://kindlegen.s3.amazonaws.com/kindlegen_linux_2.6_i386_v2_9.tar.gz
endif
	
