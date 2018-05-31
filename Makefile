SHELL = /bin/bash
DESTDIR = _site
PANDOC = pandoc

export YHY_FILTER_SRC
export YHY_FILTER_BASE = https://media.yeonghoey.com

content_src = content/%/README.org
content_dst = $(DESTDIR)/%/index.html
content_src_files = $(shell find content -type f -name 'README.org')
content_dst_files = \
	$(patsubst $(content_src),$(content_dst),$(content_src_files))

static_src = static/%
static_dst = $(DESTDIR)/%
static_src_files = $(shell find static -type f)
static_dst_files = \
	$(patsubst $(static_src),$(static_dst),$(static_src_files))


.PHONY: init dev build local sync clean

init:
	pipenv install --dev

dev: local
	pipenv run python scripts/dev.py

build: $(content_dst_files) $(static_dst_files)

local: $(content_dst_files) $(static_dst_files) sync

sync:
  # upload
	pipenv run aws s3 sync \
		'content' \
		's3://yeonghoey-media' \
		--exclude "*" \
		--include "*.png" \
		--include "*.jpg" \
		--include "*.jpeg" \
		--include "*.gif" \
		--include "*.pdf"

  # download
	pipenv run aws s3 sync \
		's3://yeonghoey-media' \
		'content'

clean:
	-rm -rf $(DESTDIR)/*

$(content_dst): YHY_FILTER_SRC = $<
$(content_dst): $(content_src)
	mkdir -p "$(dir $@)"
	@env | grep '^YHY_'
	pipenv run $(PANDOC) \
		--standalone \
		--mathjax \
		--css '/pandoc.css' \
		--filter 'scripts/filter.py' \
		--output '$@' \
		'$<'

$(static_dst): $(static_src)
	mkdir -p "$(dir $@)"
	cp '$<' '$@'
