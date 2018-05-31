SHELL = /bin/bash
DESTDIR = _site
PANDOC = pandoc

MEDIA_TYPES = png jpg jpeg gif pdf

# ==============================================================================
# Run `pandoc` from `content/**/README.org to `_site/**/index.html`
# ==============================================================================
CONTENT_SRC = content/%/README.org
CONTENT_DST = $(DESTDIR)/%/index.html
CONTENT_SRC_FILES = $(shell find 'content' -type f -name 'README.org')
CONTENT_DST_FILES = \
	$(patsubst $(CONTENT_SRC),$(CONTENT_DST),$(CONTENT_SRC_FILES))

$(CONTENT_DST): export YEONGHOEY_FILTER_BASE = https://media.yeonghoey.com
$(CONTENT_DST): export YEONGHOEY_FILTER_SRC = $<
$(CONTENT_DST): $(CONTENT_SRC)
	mkdir -p "$(dir $@)"
	pipenv run $(PANDOC) \
  --standalone \
  --mathjax \
  --css '/pandoc.css' \
  --filter 'scripts/filter.py' \
  --output '$@' \
  '$<'


# ==============================================================================
# Copy `static/**` to `$(DESTDIR)/`
# ==============================================================================
STATIC_SRC = static/%
STATIC_DST = $(DESTDIR)/%
STATIC_SRC_FILES = $(shell find static -type f)
STATIC_DST_FILES = \
	$(patsubst $(STATIC_SRC),$(STATIC_DST),$(STATIC_SRC_FILES))

$(STATIC_DST): $(STATIC_SRC)
	mkdir -p "$(dir $@)"
	cp '$<' '$@'


# ==============================================================================
# PHONY targets
# ==============================================================================
.PHONY: init ci dev sync build clean

init:
	pipenv install --dev
	pipenv run aws s3 sync 's3://yeonghoey-media' 'content'

ci:
	pipenv install

dev: sync build
	pipenv run python scripts/dev.py

build: $(CONTENT_DST_FILES) $(STATIC_DST_FILES)

sync:
  # upload
	pipenv run aws s3 sync \
  'content' \
  's3://yeonghoey-media' \
  --exclude '*' \
  $(patsubst %,--include '*.%',$(MEDIA_TYPES))

clean:
	-rm -rf $(DESTDIR)/*
