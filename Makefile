SHELL = /bin/bash

content = $(wildcard content/**/README.org)
docs    = $(patsubst content/%/README.org,docs/%/index.html,$(content))

.PHONY: all dev

all: $(docs)

docs/%/index.html: content/%/README.org
	mkdir -p "$(dir $@)"
	pandoc '$<' --mathjax -s -o '$@'

dev:
	pipenv run python dev.py
