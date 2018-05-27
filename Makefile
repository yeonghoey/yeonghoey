SHELL = /bin/bash

PANDOC = pandoc
DESTDIR = _site

export YHY_SRC_PATH ?= ''
export YHY_BASE_URL ?= \
	https://github.com/yeonghoey/yeonghoey/raw/master

# content
content_src = content/%/README.org
content_dst = $(DESTDIR)/%/index.html

content_src_files = $(shell find content -type f -name 'README.org')
content_dst_files = \
	$(patsubst $(content_src),$(content_dst),$(content_src_files))

# static
static_src = static/%
static_dst = $(DESTDIR)/%
static_src_files = $(shell find static -type f)
static_dst_files = \
	$(patsubst $(static_src),$(static_dst),$(static_src_files))


.PHONY: all update dev clean

all: $(content_dst_files) $(static_dst_files)

update:
	scripts/update.sh

dev:
	YHY_BASE_URL='' \
	$(MAKE) -j; \
	pipenv run python scripts/dev.py

clean:
	-rm -rf $(DESTDIR)/*

$(content_dst) : $(content_src)
	mkdir -p "$(dir $@)"
	YHY_SRC_PATH='$<' \
	pipenv run $(PANDOC) \
		--standalone \
		--mathjax \
		--filter 'scripts/filter.py' \
		--output '$@' \
		'$<'

$(static_dst) : $(static_src)
	cp '$<' '$@'
