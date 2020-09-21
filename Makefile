# Makefile for easier installation and cleanup.
#
# Uses self-documenting macros from here:
# http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
MAKEFLAGS += --warn-undefined-variables --no-builtin-rules

PACKAGE=readabilipy
DOC_DIR=./docs
VENV_DIR=/tmp/rdpy_venv
TEST_DIR=./tests

.PHONY: help

.DEFAULT_GOAL := help

# Display a help message when called without target, using the ## comments
help:
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) |\
		 awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m\
		 %s\n", $$1, $$2}'

################
# Installation #
################

.PHONY: install

install: ## Install for the current user using the default python command
	python setup.py build_ext --inplace
	python setup.py install --user


################
# Distribution #
################

.PHONY: release dist

release: ## Make a release
	python make_release.py

dist: ## Make Python source distribution
	python setup.py sdist bdist_wheel


###########
# Testing #
###########

.PHONY: test

test: venv ## Run unit tests
	source $(VENV_DIR)/bin/activate && cd $(TEST_DIR) && \
		python -m pytest -v . --cov readabilipy \
		--cov-report term-missing --benchmark-disable
	source $(VENV_DIR)/bin/activate && pyflakes *.py readabilipy $(TEST_DIR)
	source $(VENV_DIR)/bin/activate && pycodestyle --statistics \
		--ignore=E501 --count *.py readabilipy $(TEST_DIR)
	source $(VENV_DIR)/bin/activate && pylint readabilipy $(TEST_DIR)/*.py

#################
# Documentation #
#################

.PHONY: docs

docs: install ## Build documentation with Sphinx
	exit; # not implemented
	source $(VENV_DIR)/bin/activate && m2r README.md && mv README.rst $(DOC_DIR)
	source $(VENV_DIR)/bin/activate && m2r CHANGELOG.md && mv CHANGELOG.rst $(DOC_DIR)
	cd $(DOC_DIR) && \
		rm source/* && \
		source $(VENV_DIR)/bin/activate && \
		sphinx-apidoc -H 'ReadabiliPy API Documentation' -o source ../$(PACKAGE) && \
		touch source/AUTOGENERATED
	$(MAKE) -C $(DOC_DIR) html

#######################
# Virtual environment #
#######################

.PHONY: venv

venv: $(VENV_DIR)/bin/activate

$(VENV_DIR)/bin/activate: setup.py
	test -d $(VENV_DIR) || python -m venv $(VENV_DIR)
	source $(VENV_DIR)/bin/activate && pip install .[dev]
	touch $(VENV_DIR)/bin/activate

############
# Clean up #
############

.PHONY: clean

clean: ## Clean build dist and egg directories left after install
	rm -rf ./dist
	rm -rf ./build
	rm -rf ./$(PACKAGE).egg-info
	rm -rf $(VENV_DIR)
	rm -f MANIFEST
	rm -rf $(PACKAGE)/javascript/node_modules
	find . -type f -iname '*.pyc' -delete
	find . -type d -name '__pycache__' -empty -delete
