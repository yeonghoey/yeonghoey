SHELL = /bin/bash
DESTDIR = _site
PANDOC = pandoc

MEDIA_TYPES = png jpg jpeg gif pdf

# ==============================================================================
# Run `pandoc` from `content/**/README.org to `_site/**/index.html`
# ==============================================================================

CONTENT_SRC = $(shell find 'content' -type f -name 'README.org')
CONTENT_DST = $(CONTENT_SRC:content/%/README.org=$(DESTDIR)/%/index.html)

export YEONGHOEY_FILTER_SRC
export YEONGHOEY_FILTER_MEDIA
$(CONTENT_DST): YEONGHOEY_FILTER_SRC = $<
$(CONTENT_DST): $(DESTDIR)/%/index.html : content/%/README.org
	mkdir -p "$(dir $@)"
	@env | grep YEONGHOEY_
	pipenv run $(PANDOC) \
  --standalone \
  --mathjax \
  --template='templates/content.html' \
  --filter='scripts/filter.py' \
  --output='$@' \
  '$<'


# ==============================================================================
# Make symlinks of content local directories (prefixed with '_' like '_img')
# for dev server
# ==============================================================================
LOCAL_SRC = $(shell find content -type d -name '_*')
LOCAL_DST = $(LOCAL_SRC:content/%=$(DESTDIR)/%)

$(LOCAL_DST): $(DESTDIR)/%: content/%
	mkdir -p "$(dir $@)"
	ln -sf '$(abspath $<)' '$@'


# ==============================================================================
# Copy `static/**` to `$(DESTDIR)/`
# ==============================================================================
STATIC_SRC = $(shell find 'static' -type f)
STATIC_DST = $(STATIC_SRC:static/%=$(DESTDIR)/%)

$(STATIC_DST): $(DESTDIR)/%: static/%
	mkdir -p "$(dir $@)"
	cp '$<' '$@'


# ==============================================================================
# PHONY targets
# ==============================================================================
.PHONY: init ci update build local sync sync-down sync-up prune dev clean

init:
	pipenv install --dev
	cp scripts/pre-push .git/hooks/

ci:
	pipenv install

update:
	git pull --rebase --autostash

build: YEONGHOEY_FILTER_MEDIA = https://media.yeonghoey.com
build: $(CONTENT_DST) $(STATIC_DST)

local: YEONGHOEY_FILTER_MEDIA =
local: $(CONTENT_DST) $(STATIC_DST) $(LOCAL_DST)

sync: sync-down sync-up

sync-down:
	pipenv run aws s3 sync \
  's3://yeonghoey-media' \
  'content'

sync-up:
	pipenv run aws s3 sync \
  'content' \
  's3://yeonghoey-media' \
  --exclude '*' \
  $(patsubst %,--include '*.%',$(MEDIA_TYPES)) \
  $(YEONGHOEY_SYNCFLAGS)

prune: YEONGHOEY_SYNCFLAGS = --delete --dryrun
prune: sync-up

dev: local
	pipenv run python scripts/dev.py

clean:
	-rm -rf $(DESTDIR)/*
