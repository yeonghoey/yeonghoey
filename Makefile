SHELL = /bin/bash
DESTDIR = _site
TEMPDIR = _temp
PANDOC = pandoc

MEDIA_TYPES = png jpg jpeg gif pdf

# ==============================================================================
# Pandoc Recipe
# ==============================================================================
export YEONGHOEY_FILTER_SRC
export YEONGHOEY_FILTER_MEDIA

define run-pandoc
mkdir -p "$(dir $@)"
@env | grep 'YEONGHOEY_'
pipenv run $(PANDOC) \
--standalone \
--mathjax \
$(cssflags) \
--template='resources/content.html' \
--include-in-header='resources/fonts.html' \
--include-before-body='$(navfile)' \
--filter='scripts/filter.py' \
$(1) \
--output='$@' \
'$<'
endef

cssflags = $(patsubst $(DESTDIR)%,--css='%',$(SCSS_DST))
navfile  = $(patsubst $(DESTDIR)%index.html,$(TEMPDIR)%nav.html,$@)


# ==============================================================================
# S3 Push Recipe
# ==============================================================================
define run-s3push
pipenv run aws s3 sync \
'content/$(1)' \
's3://yeonghoey-media/$(1)' \
--exclude '*' \
$(patsubst %,--include '*.%',$(MEDIA_TYPES)) \
$(YEONGHOEY_SYNCFLAGS)
endef

# ==============================================================================
# Compile SCSS
# ==============================================================================
SCSS_SRC = $(shell find 'resources' -type f -name '*.scss')
SCSS_DST = $(SCSS_SRC:resources/%.scss=$(DESTDIR)/_css/%.css)
$(SCSS_DST):
$(DESTDIR)/_css/%.css : resources/%.scss
	mkdir -p "$(dir $@)"
	pipenv run sassc $< $@


# ==============================================================================
# Generate /index.html
# ==============================================================================
INDEX_SRC = README.org resources/index.org content scripts/index.py

$(DESTDIR)/index.html: YEONGHOEY_FILTER_SRC = $<
$(DESTDIR)/index.html: $(TEMPDIR)/index.org $(TEMPDIR)/nav.html
	$(call run-pandoc)

$(TEMPDIR)/index.org: $(INDEX_SRC)
	mkdir -p "$(dir $@)"
	pipenv run python 'scripts/index.py' '$@'

$(TEMPDIR)/nav.html: $(INDEX_SRC)
	mkdir -p "$(dir $@)"
	pipenv run python 'scripts/nav.py' "$@"

# ==============================================================================
# Run `pandoc` from `content/**/README.org to `_site/**/index.html`
# ==============================================================================

CONTENT_SRC = $(shell find 'content' -type f -name 'README.org')
CONTENT_NAV = $(CONTENT_SRC:content/%/README.org=$(TEMPDIR)/%/nav.html)
CONTENT_DST = $(CONTENT_SRC:content/%/README.org=$(DESTDIR)/%/index.html)

$(CONTENT_NAV): \
$(TEMPDIR)/%/nav.html : content/%/README.org
	mkdir -p "$(dir $@)"
	pipenv run python 'scripts/nav.py' "$@"

$(CONTENT_DST): YEONGHOEY_FILTER_SRC = $<
$(CONTENT_DST): \
$(DESTDIR)/%/index.html : content/%/README.org $(TEMPDIR)/%/nav.html
	$(call run-pandoc,--table-of-contents)


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
# Publish changed content's media files
# ==============================================================================
CHANGED_FILES = $(shell git diff --name-only origin/master..HEAD)
PUBLISH_SRC = $(filter content/%/README.org,$(CHANGED_FILES))
PUBLISH_DST = $(PUBLISH_SRC:content/%/README.org=%)
$(PUBLISH_DST): % : content/%/README.org
	$(call run-s3push,$@)


# ==============================================================================
# PHONY targets
# ==============================================================================
.PHONY: ci build init local dev publish s3pull s3push clean

ci:
	pipenv install

build: YEONGHOEY_FILTER_MEDIA = https://media.yeonghoey.com
build: \
  $(STATIC_DST) $(SCSS_DST) $(DESTDIR)/index.html $(CONTENT_DST)

init: s3pull
	pipenv install --dev
	cp scripts/pre-push .git/hooks/

local: YEONGHOEY_FILTER_MEDIA =
local: \
  $(STATIC_DST) $(SCSS_DST) $(DESTDIR)/index.html $(CONTENT_DST) $(LOCAL_DST)

dev: local
	pipenv run python scripts/dev.py

publish: $(PUBLISH_DST)

s3pull:
	pipenv run aws s3 sync \
  's3://yeonghoey-media' \
  'content'

s3push:
	$(call run-s3push)

clean:
	-rm -rf $(DESTDIR)/*
